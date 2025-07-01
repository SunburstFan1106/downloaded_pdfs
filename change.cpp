#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <regex>
#include <algorithm>
#include <locale>
#include <codecvt>
#include <cstring>

class StudentSchoolConverter {
private:
    std::map<std::string, std::set<std::string>> studentSchoolMap;
    
    // 清理学校名称
    std::string cleanSchoolName(const std::string& schoolName) {
        std::string cleaned = schoolName;
        
        // 移除常见前缀
        if (cleaned.find("上海市") == 0) {
            cleaned = cleaned.substr(9); // UTF-8中文字符占3字节
        } else if (cleaned.find("上海") == 0) {
            cleaned = cleaned.substr(6); // UTF-8中文字符占3字节
        }
        
        // 特殊处理映射
        std::map<std::string, std::string> replacements = {
            {"华东师范大学第二附属中学", "华二附中"},
            {"华东师范大学第三附属中学", "华三附中"},
            {"复旦大学附属中学", "复旦附中"},
            {"上海交通大学附属中学", "交大附中"},
            {"曹杨第二中学国际课程班预录取名单(1)", "曹杨二中"},
            {"曹杨第二中学", "曹杨二中"},
            {"复旦大学附属复兴中学", "复旦复兴中学"}
        };
        
        for (const auto& pair : replacements) {
            if (cleaned.find(pair.first) != std::string::npos) {
                cleaned = pair.second;
                break;
            }
        }
        
        return cleaned;
    }
    
    // 从文件名中提取学校名称
    std::string extractSchoolFromFilename(const std::string& filename) {
        std::regex pattern("2025年(.+?)(?:_\\d+)?\\.pdf");
        std::smatch match;
        
        if (std::regex_search(filename, match, pattern)) {
            return cleanSchoolName(match[1].str());
        }
        
        return "";
    }
    
    // 去除字符串首尾空格
    std::string trim(const std::string& str) {
        size_t start = str.find_first_not_of(" \t\r\n");
        if (start == std::string::npos) return "";
        
        size_t end = str.find_last_not_of(" \t\r\n");
        return str.substr(start, end - start + 1);
    }
    
    // 检查是否是学生姓名行
    bool isStudentNameLine(const std::string& line, std::string& studentName) {
        // 查找模式：在以下文件中找到"姓名"：
        std::string prefix = "在以下文件中找到\"";
        size_t start = line.find(prefix);
        if (start == std::string::npos) return false;
        
        start += prefix.length();
        size_t end = line.find("\"：", start);
        if (end == std::string::npos) return false;
        
        studentName = line.substr(start, end - start);
        return !studentName.empty();
    }
    
public:
    // 解析输入文件
    bool parseInputFile(const std::string& filename) {
        std::ifstream file(filename, std::ios::in);
        if (!file.is_open()) {
            std::cerr << "错误：无法打开文件 " << filename << std::endl;
            return false;
        }
        
        std::string line;
        std::string currentStudent = "";
        
        while (std::getline(file, line)) {
            line = trim(line);
            if (line.empty()) continue;
            
            std::string studentName;
            // 检查是否是学生姓名行
            if (isStudentNameLine(line, studentName)) {
                currentStudent = studentName;
                studentSchoolMap[currentStudent] = std::set<std::string>();
            }
            // 检查是否是文件名行
            else if (!currentStudent.empty() && line.find("2025年") != std::string::npos) {
                std::string school = extractSchoolFromFilename(line);
                if (!school.empty()) {
                    studentSchoolMap[currentStudent].insert(school);
                }
            }
        }
        
        file.close();
        return true;
    }
    
    // 生成输出
    void generateOutput(const std::string& outputFilename) {
        std::ofstream outFile(outputFilename, std::ios::out);
        if (!outFile.is_open()) {
            std::cerr << "错误：无法创建输出文件 " << outputFilename << std::endl;
            return;
        }
        
        // 写入文件头
        outFile << "学生名单（人名 学校格式）" << std::endl;
        outFile << std::string(50, '=') << std::endl << std::endl;
        
        // 生成学生-学校对应列表
        std::vector<std::string> results;
        
        for (const auto& pair : studentSchoolMap) {
            const std::string& studentName = pair.first;
            const std::set<std::string>& schools = pair.second;
            
            if (schools.empty()) {
                results.push_back(studentName + " 未知学校");
            } else {
                // 将所有学校连接成字符串
                std::string schoolList = "";
                bool first = true;
                for (const std::string& school : schools) {
                    if (!first) schoolList += ", ";
                    schoolList += school;
                    first = false;
                }
                results.push_back(studentName + " " + schoolList);
            }
        }
        
        // 排序结果
        std::sort(results.begin(), results.end());
        
        // 写入文件和控制台输出
        std::cout << "转换结果：" << std::endl;
        std::cout << std::string(40, '=') << std::endl;
        
        for (const std::string& result : results) {
            outFile << result << std::endl;
            std::cout << result << std::endl;
        }
        
        outFile.close();
        
        std::cout << std::endl << "转换完成！" << std::endl;
        std::cout << "输出文件：" << outputFilename << std::endl;
        std::cout << "总计：" << results.size() << " 名学生" << std::endl;
    }
    
    // 生成统计信息
    void generateStatistics() {
        std::map<std::string, int> schoolCount;
        
        for (const auto& pair : studentSchoolMap) {
            for (const std::string& school : pair.second) {
                schoolCount[school]++;
            }
        }
        
        std::cout << std::endl << "学校统计：" << std::endl;
        std::cout << std::string(30, '-') << std::endl;
        
        // 按学生数量排序
        std::vector<std::pair<std::string, int>> sortedSchools(schoolCount.begin(), schoolCount.end());
        std::sort(sortedSchools.begin(), sortedSchools.end(), 
                  [](const std::pair<std::string, int>& a, const std::pair<std::string, int>& b) { 
                      return a.second > b.second; 
                  });
        
        for (const auto& pair : sortedSchools) {
            std::cout << pair.first << ": " << pair.second << " 人" << std::endl;
        }
    }
};

int main() {
    // 设置控制台输出编码（Windows）
    #ifdef _WIN32
    system("chcp 65001 > nul");
    #endif
    
    std::cout << "学生名单格式转换工具 (C++版本)" << std::endl;
    std::cout << std::string(50, '=') << std::endl;
    
    StudentSchoolConverter converter;
    
    // 解析输入文件
    std::string inputFile = "out.txt";
    if (!converter.parseInputFile(inputFile)) {
        std::cerr << "解析输入文件失败！" << std::endl;
        return 1;
    }
    
    // 生成输出
    std::string outputFile = "name_school_list_cpp.txt";
    converter.generateOutput(outputFile);
    
    // 生成统计信息
    converter.generateStatistics();
    
    return 0;
}
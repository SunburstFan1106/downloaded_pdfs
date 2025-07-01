# 读取文件内容并转换格式，处理分校情况
$inputFile = "c:\Users\cyez-oi\Downloads\downloaded_pdfs\out.txt"
$outputFile = "c:\Users\cyez-oi\Downloads\downloaded_pdfs\formatted_list.txt"

# 读取所有行
$content = Get-Content $inputFile -Encoding UTF8

$result = @()
$currentName = ""

for ($i = 0; $i -lt $content.Length; $i++) {
    $line = $content[$i].Trim()
    
    # 检查是否是姓名行
    if ($line -match '在以下文件中找到"([^"]+)"：') {
        $currentName = $matches[1]
    }
    # 检查是否是学校文件行
    elseif ($line -match '^\d{4}年(.+)_\d+\.pdf$' -and $currentName -ne "") {
        $school = $matches[1]
        $result += "$currentName $school"
    }
    # 处理国际课程班等特殊情况
    elseif ($line -match '^\d{4}年(.+)\.pdf$' -and $currentName -ne "") {
        $school = $matches[1]
        $result += "$currentName $school"
    }
}

# 去重并排序
$result = $result | Sort-Object | Get-Unique

# 输出到文件
$result | Out-File $outputFile -Encoding UTF8

Write-Host "转换完成！结果已保存到: $outputFile"
Write-Host "共处理了 $($result.Count) 条记录"

# 显示包含分校的记录
Write-Host "`n包含分校/特殊标识的记录："
$result | Where-Object { $_ -match "(第[一二三四五]附属|附属.+中学|国际课程班)" } | Sort-Object
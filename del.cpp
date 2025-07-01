#include<bits/stdc++.h>
using namespace std;

int main(){
    freopen("1.txt","r",stdin);
    freopen("testtttt.ans","w",stdout);
    string s;
    while(cin>>s){
        if(!s.find("未")){
            continue;
        }
        else cout<< s << endl;
    }

    return 0;
}
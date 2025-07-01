#include<bits/stdc++.h>
using namespace std;

int main(){
    freopen("list.txt","r",stdin);
    freopen("out.txt","w",stdout);
    string s;
    while(cin>>s){
        if(!s.find("未")){
            continue;
        }
        else cout<< s << endl;
    }

    return 0;
}
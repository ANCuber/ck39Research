#include <bits/stdc++.h>
using namespace std;

#define endl '\n'

string five_con_list[5][2] = {{"[Peql]","等於"},{"[Ples]","小於"},{"[Pbgr]","大於"},{"[Pbeg]leq[Pspa]","小於等於"},{"[Pbeg]geq[Pspa]","大於等於"}};


int main()
{
    ios::sync_with_stdio(0), cin.tie(0), cout.tie(0);
    srand(time(NULL));
    for (int i = 0; i < 750; ++i) {
        int cur = rand()%5;
        //string a = to_string(rand()%100000);
        string a; cin>>a;
        string b = to_string(rand()%100000);
        cout<<a<<five_con_list[cur][0]<<b<<"\|\|,\|\|"<<a<<five_con_list[cur][1]<<b<<endl;
    }
    for (int i = 0; i < 750; ++i) {
        int cur = rand()%5;
        string a = to_string(rand()%100000);
        //string b = to_string(rand()%100000);
        string b; cin>>b;
        cout<<a<<five_con_list[cur][0]<<b<<"\|\|,\|\|"<<a<<five_con_list[cur][1]<<b<<endl;
    }
}

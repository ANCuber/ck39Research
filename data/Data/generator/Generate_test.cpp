#include <bits/stdc++.h>
using namespace std;
#define cout outf
char arr[] = {'^','+','-','*','/'}; 
char variable_list[] = {'x','m','n','y','z','w','k','p','a','b','c','d','q','t','R','r','s'};
int SizeOfVarList = 17;
ofstream outf;


struct Node{
    int depth;
    bool type;
    char ope;
    Node* lc = nullptr;
    Node* rc = nullptr;
    
    void init() {
        int rd = rand()%(depth+1);
        type = !(rd <= 1);
        if (type) {
            if (rand()%2) ope = variable_list[rand()%SizeOfVarList];
            else ope = '0'+rand()%10;
        } else {
            ope = arr[rand()%5];
            if(ope=='*') ope=='$';
            lc = new Node, rc = new Node;
            lc->depth = rc->depth = depth+1;
            lc->init(), rc->init();
            if(lc->type && rc->type && rc->ope>='0' && rc->ope<='9') swap(lc,rc);
        }
    }
    
};


void dfs(Node* cur) {
    if (!cur) return;
    if (cur->type) {
        if(cur->ope>='0' && cur->ope<='9') cout<<cur->ope;
        else cout<<"{"<<(cur->ope)<<"}";
    } else {
        if(cur->ope=='/'){
           cout<<"{\\frac";
           dfs(cur->lc);
           dfs(cur->rc);
           cout<<"}";
        }else{
        cout<<'{';
        dfs(cur->lc);
        if(cur->ope!='$') cout<<(cur->ope);
        dfs(cur->rc);
        cout<<'}';
        }
    }
}

int main() {
    outf.open("gendata.txt");
    srand( time(NULL) ); 
    for(int i=0;i<100000;i++){
    Node* root = new Node;
    root->depth = 0;
    root->init();
    dfs(root);
    cout<<"\n";
    }
    return 0;
}
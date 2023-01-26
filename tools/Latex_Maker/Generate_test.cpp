#include <bits/stdc++.h>
using namespace std;
#define cout outf
char arr[] = {'^','+','-','*','/','l'}; 
char unit[] = {'q','s','c','t'};//sqrt,sin,cos,tan
map<char,string> unitmp = {{'q',"\\sqrt{"},{'s',"\\sin{"},{'c',"\\cos{"},{'t',"\\tan{"}};
char variable_list[] = {'x','m','n','y','z','w','k','p','a','b','c','d','q','t','R','r','s','%'};
int SizeOfVarList = 18, bin = 6, uni = 4;
ofstream outf;
const int sz_k = 0;
const int amount = 250;
const int prounit = 5;

struct Node{
    int depth;
    int type;
    char ope;
    Node* lc = nullptr;
    Node* rc = nullptr;
    
    void init() {
        int rd = rand()%(depth+1);
        type = !(rd <= sz_k);
        if (type) {
            if (rand()%2) ope = variable_list[rand()%SizeOfVarList];
            else ope = '0'+rand()%10;
        } else {
            rd = rand()%prounit;
            if (rd == 0) {//unit
                type = 0;
                ope = unit[rand()%uni];
                lc = new Node, rc = nullptr;
                lc->depth = depth+1;
                lc->init();
            } else {
                type = 2;
                ope = arr[rand()%bin];
                if(ope=='*') ope = '$';
                lc = new Node, rc = new Node;
                lc->depth = rc->depth = depth+1;
                lc->init(), rc->init();
                if(lc->type && rc->type && rc->ope>='0' && rc->ope<='9') swap(lc,rc);
            }
        }
    }
    
};


void dfs(Node* cur,bool enclose) {
    if (!cur) return;
    if (cur->type == 2){
        if (cur->ope == 'l') {
            cout<<"\\log_{";
            dfs(cur->lc,0);
            cout<<"}";
            dfs(cur->rc,1);
        } else if(cur->ope=='/'){
            cout<<"\\frac{";
            dfs(cur->lc,0);
            cout<<"}{";
            dfs(cur->rc,0);
            cout<<"}";
        } else if(cur->ope=='^'){
            cout<<"{";
            dfs(cur->lc,0);
            cout<<"}^{";
            dfs(cur->rc,0);
            cout<<"}";
        } else {
            if(enclose) cout<<'(';
            dfs(cur->lc,1);
            if(cur->ope!='$') cout<<(cur->ope);
            dfs(cur->rc,1);
            if(enclose) cout<<')';
        }
    } else if (cur->type == 1) {
        //cout<<"{"<<(cur->ope)<<"}";
        if (cur->ope == '%') cout<<"\\pi ";
        else cout<<(cur->ope);
    } else {
        if (enclose) cout<<'(';
        cout<<unitmp[cur->ope];
        dfs(cur->lc,0);
        cout<<"}";
        if (enclose) cout<<')';
    }
}

int main() {
    outf.open("gendata.txt");
    srand( time(0) ); 
    for(int i=0;i < amount;i++){
        Node* root = new Node;
        root->depth = 0;
        root->init();
        dfs(root,0);
        cout<<"\n";
    }
    return 0;
}
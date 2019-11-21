#include<iostream>
#include<sstream>
#include <vector>
#include <memory>
#include <stack>
#include <algorithm>
#include <bits/stdc++.h>

using namespace std;



void run(istream &input, ostream &output) {
    size_t count;
    input >> count;
    std::set<int, greater<int>> stroy;
    int command;
    uint32_t data;
    for (int i = 0; i < count; ++i) {
        input >> command >> data;
        if (command == 1) {
            stroy.insert(data);
            cout << distance( stroy.begin(), stroy.find(data) ) << endl;
        } else {
            stroy.erase(next(begin(stroy),data));
                    //stroy.erase(advance(stroy.begin(),data));
        }
    }
}

    void testLogic() {
//    {
//        stringstream input;
//        stringstream output;
//        input << "5" << endl;
//        input << "1 100" << endl;
//        input << "1 200" << endl;
//        input << "1 50" << endl;
//        input << "2 1" << endl;
//        input << "1 150" << endl;
//        run(input, output);
//        cout << "*************************" << endl;
//    }
//    {
//        stringstream input;
//        stringstream output;
//        input << "13" << endl;
//        input << "1 100" << endl;//0
//        input << "1 200" << endl;//0
//        input << "1 120" << endl;//1
//        input << "1 30" << endl;//3
//        input << "1 125" << endl;//1
//        input << "1 50" << endl;//4
//        input << "2 4" << endl;//delete 50
//        input << "2 3" << endl;//del 100
//        input << "2 0" << endl;//del 200
//        input << "1 110" << endl;//2
//        input << "1 20" << endl;//4
//        input << "2 0" << endl;//delete 120
//        input << "1 115" << endl;//1
//        run(input, output);
//        cout << "*************************" << endl;
//    }
        {
            stringstream input;
            stringstream output;
            input << "21" << endl;
            input << "1 100" << endl;//0
            input << "1 200" << endl;//0
            input << "1 120" << endl;//1
            input << "1 30" << endl;//3
            input << "1 125" << endl;//1
            input << "1 50" << endl;//4
            input << "1 70" << endl;//4
            input << "1 1700" << endl;//0
            input << "1 170" << endl;//2
            input << "1 37" << endl;//8
            input << "2 4" << endl;//del 120
            input << "1 124" << endl;//4
            input << "2 2" << endl;//4
            input << "2 3" << endl;//4
            input << "2 0" << endl;//4
            input << "2 2" << endl;//4
            input << "2 1" << endl;//4
            input << "2 0" << endl;//4
            input << "1 1" << endl;//2
            input << "2 0" << endl;//4
            input << "1 2" << endl;//2
            run(input, output);
            cout << "*************************" << endl;
        }

    }

    int main(int argc, const char *argv[]) {
        testLogic();
        //run(cin, cout);
        return 0;
    }
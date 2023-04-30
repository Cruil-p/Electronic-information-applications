#include <iostream>
#include <algorithm>
#include <cstring>
#include <queue>
#include <fstream>
#include <vector>

using namespace std;

const int N = 1e8 + 10;

int n, idx, idx2;
int num; // the num of nodes whose leaf has more than one child
int leaf;// the num of leaf
int* h = new int[N];
int* e = new int[N];
int* ne = new int[N];
int* s = new int[N];
int* cluster = new int[N];
int* centerids = new int[N];
int* childStarts = new int[N];
int* childEnds = new int[N];
int* s2 = new int[N];
queue<int> q;
vector<int>* v = new vector<int>[N];

void add(int a, int b)
{
	e[idx] = b, ne[idx] = h[a], h[a] = idx ++;
}

int dfs(int u)
{
	for (int i = h[u]; ~i; i = ne[i])
	{
		int j = e[i];
		s[j] = dfs(j);
		s[u] += s[j];
	}
	return s[u] + 1;
}

void bfs(int u)
{
	q.push(u);
	while(q.size())
	{
		bool flag = false;
		int t = q.front(); q.pop();
		num ++;
		for (int i = h[t]; ~i; i = ne[i])
		{
			int j = e[i];
			if (s[j] > 1)
			{
				flag = true;
				q.push(j);
			}
			else leaf ++;
		}
		if (!flag)
		{
			cluster[idx2] = t;
			v[idx2].push_back(t);
			for (int i = h[t]; ~i; i = ne[i] )
			{
				int j = e[i];
				v[idx2].push_back(j);
			}
			idx2 ++;
		}
	}
}

void get_centerids_and_nodes(int number)
{
	for (int i = 0; i < idx2; i ++ )
        {
                if (v[i].size() < number)
		{
                        for (auto c: v[i])
                                cout << c << " ";
                	cout << endl;
		}
        }
}

void print_to_txt()
{
	ofstream outfile;
	string path2 = "./out/outfile.txt";
	outfile.open(path2);
	// outfile << idx2 << endl;
	for (int i = 0; i < idx2; i ++ )
	{
		int jj = 0;
		for (auto c: v[i])
		{
			if (jj == 0) outfile << c;
			else outfile << " " << c ;
			jj ++;
		}
		if (i != idx2 - 1)
			outfile << endl;
	}		
	outfile.close();	
}

int main()
{
    
	// memset(h, -1, (N - 2) * sizeof(h));
        string path1 = "./out/log.txt";
	ifstream fin(path1, ios::in);
	fin >> n;
	// cout << "address of h: " << &h << endl;
	memset(h, -1, sizeof(int) * N);
	int root = n;
	for (int i = 0; i < n; i ++ )
	    fin >> centerids[i];
	for (int i = 0; i < n; i ++ )
	    fin >> childStarts[i];
	for (int i = 0; i < n; i ++ )
            fin >> childEnds[i];

	for (int i = childStarts[0]; i < childEnds[0]; i ++ )
		add(root, centerids[i]);
	for (int i = 1; i < n; i ++)
		for (int j = childStarts[i]; j < childEnds[i]; j ++ )
			add(centerids[i], centerids[j]);
	
	// for (int i = 0; i < n + 1; i ++ )s[i] = 0;
	// int root = n;
	
	s[root] = dfs(root);
	
	bfs(root);
	
	// for (int i = 0; i < idx2; i ++ )
		// cout << cluster[i] << " ";
	// cout << endl;
	// memcpy(s2, s, sizeof s);

	int sum = 0; 
	for (int i = 0; i < idx2; i ++ ) sum += s[cluster[i]];	
	cout << "centerids count: " << idx2 << endl;
	cout << "cluster nodes nums: " << sum << endl;
	for (int i = 0; i < idx2; i ++ ) s2[i] = s[cluster[i]];
	sort(s2, s2 + idx2);
	
	double sum1 = 0;
	for (int i = 0; i < idx2; i ++ ) sum1 += s2[i];
	double avg = sum1 / idx2;
	double means = 0;
	for (int i = 0; i < idx2; i ++ )
	     means += (avg - s2[i]) * (avg - s2[i]);
	means /= idx2;

	// for (int i = 0; i < idx2; i ++ )cout << s2[i] << " " ;
	// cout << endl;
	// cout << "num means: " << means << endl;
	// cout << "more children root num: " << num << endl;
	// cout << "leaf num: " << leaf << endl; 

	// int num = 100;
	// get_centerids_and_nodes(num); // print the centerids whose leaf-numbers less or equal than the num; 
	
	
	// print into txt 
	print_to_txt();
	
	
	return 0;
} 

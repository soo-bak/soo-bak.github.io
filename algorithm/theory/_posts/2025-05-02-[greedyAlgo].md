---
layout: single
title: "그리디 알고리듬(Greedy Algorithm, 탐욕법)의 원리와 적용 - soo:bak"
date: "2025-05-02 06:30:00 +0900"
description: 순간의 최적을 선택하는 그리디 알고리듬의 개념과 적용 조건, 예제 코드를 통한 실전 활용법을 이해하기 쉽게 설명
---

## 그리디 알고리듬이란?

**그리디 알고리듬(Greedy Algorithm, 탐욕법)**은 문제 해결 과정에서 `현재 순간에 가장 최선이라고 판단되는 선택`을 반복적으로 수행하여 전체 해답을 구하는 방식입니다.

여기서, '최선의 선택'이란 단순히 당장의 선택 순간에서 이득을 극대화하거나 비용을 최소화하는 결정을 의미합니다.

즉, 전체적인 흐름이나 미래 상황까지 고려하지는 않습니다.

<br>
**이전 선택의 결과**를 기억하거나 **전체 경로**를 추적하지도 않으며,

단순히 각 단계에서 가장 유리해 보이는 선택을 고정하여 해를 쌓아나가는 구조 덕분에 구현이 간단하고 계산량도 적은 경우가 많습니다.

다만, 항상 정답을 보장하지 않는다는 점을 염두하여 문제의 구조와 조건에 대해서 그리디 선택이 전체 최적해로 이어지는지를 미리 검토해야 합니다.

<br>

## 작동 방식과 특징

그리디 알고리듬의 처리 과정은 다음과 같습니다:

- 문제를 여러 부분(단계)으로 분할
- 각 단계에서 가능한 선택지 중 `가장 좋아 보이는 선택`을 하나 선택
- 선택한 결과는 고정하고, 다음 단계로 넘어감
- 이러한 선택 과정을 반복하며 최종 해답을 구성

<br>
즉, 그리디 알고리듬은 한 번 선택한 내용은 다시 수정하지 않으며,

되돌아가거나 새로운 대안을 고려하는 백트래킹이나 동적 계획법과는 달리 단방향으로만 진행합니다.

<br>
이러한 구조로 다음과 같은 장점과 단점이 존재합니다:

- ✅ **장점**: 구현이 간단하고 빠르며, 직관적으로 이해하기 쉬움
- ⚠️ **단점**: `국소 최적(Local Optimum)`이 반드시 `전체 최적(Global Optimum)`이 된다는 보장이 없으므로, 문제에 따라 잘못된 결과를 낼 수 있음

<br>
### 적용 가능한 조건
그리디 알고리듬이 항상 정답을 구할 수 있으려면, 다음의 두 조건이 반드시 성립해야 합니다:

**탐욕적 선택 속성(Greedy Choice Property)** <br>
각 단계에서의 선택이 전체 최적해의 일부가 되어야 합니다.<br>
즉, 지금의 최선 선택이 미래의 최적해 구성을 방해하지 않아야 합니다.

**최적 부분 구조(Optimal Substructure)** <br>
전체 문제의 최적해는 부분 문제들의 최적해를 조합하여 얻을 수 있어야 합니다.<br>
이 조건은 동적 계획법(DP)과도 유사하지만, 중요한 차이점이 있습니다.<br>
(DP는 **모든 부분해를 다 계산하고 비교하여 최종 선택을 결정**하는 반면, 그리디는 **순간의 판단만으로 즉시 결정**을 내립니다.)

<br>
### 그리디 알고리듬의 수학적 해석
그리디 알고리듬은 선택의 비용이나 이득이 정렬된 순서에 따라 일정하게(단조적으로) 증가하거나 감소하는 구조일 때 특히 효과적으로 동작합니다.

예시:
- 회의 일정을 종료 시간 기준으로 정렬해 가장 먼저 끝나는 회의부터 선택
- 간선을 가중치 순으로 정렬해 작은 것부터 연결
- 가치 대비 무게 비율이 높은 순으로 물건을 정렬하여 가방에 담는 전략

<br>
이처럼 그리디 알고리듬은 **탐욕적 기준(greedy criterion)**에 따라 데이터를 정렬한 뒤,

그 순서대로 조건을 만족하는 선택을 차례로 수행하는 방식으로 자주 사용됩니다.

특히, 이 정렬 기준이 문제의 최적 조건과 정확히 맞아떨어질 때 효율적이고 정확한 결과를 도출합니다.

<br>

## 대표 문제 예시
다음은 실제로 그리디 알고리듬이 널리 사용되는 대표적인 문제 유형들입니다:

### 동전 거스름돈 문제
- 목표: 가장 적은 수의 동전으로 거스름돈을 만드는 문제
- 전제 조건: 동전 단위가 배수 관계를 가질 경우(예: `1`, `5`, `10`, `50`, `100`, `500`)
- 방식: 가장 큰 단위의 동전부터 차례로 최대한 많이 사용

```cpp
#include <bits/stdc++.h>
using namespace std;

int coinChangeGreedy(vector<int>& coins, int amount) {
  // 내림차순 정렬
  sort(coins.begin(), coins.end(), greater<int>());

  int count = 0;
  for (int coin : coins) {
    while (amount >= coin) {
      amount -= coin;
      count++;
    }
  }

  return count;
}

int main() {
  vector<int> coins = {500, 100, 50, 10, 5, 1};
  int amount = 1260;

  int result = coinChangeGreedy(coins, amount);
  cout << "Number of coins needed: " << result << "\n";

  return 0;
}
```

<br>

### 활동 선택 문제 (Activity Selection)
- 목표: 가장 많은 수의 활동을 선택
- 조건: 각 활동은 시작/종료 시간이 주어지며, 활동 간에 시간이 겹치면 안 됨
- 방식: 활동을 종료 시간 기준으로 정렬한 후, 가장 빨리 끝나는 활동부터 선택

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Activity {
  int start;
  int end;

  friend ostream& operator<<(ostream& os, const Activity& activity) {
    os << "(" << activity.start << ", " << activity.end << ")";
    return os;
  }
};

vector<Activity> activitySelection(vector<Activity>& activities) {
  // 종료 시간 기준으로 정렬
  sort(activities.begin(), activities.end(),
    [](const Activity& a, const Activity& b) {
      return a.end < b.end;
    });

  vector<Activity> selected;

  // 첫 번째 활동 선택
  if (!activities.empty()) {
    selected.push_back(activities[0]);
    int lastEndTime = activities[0].end;

    // 나머지 활동들 중에서 선택
    for (size_t i = 1; i < activities.size(); i++) {
      // 이전 활동이 끝난 후 시작하는 활동만 선택
      if (activities[i].start >= lastEndTime) {
        selected.push_back(activities[i]);
        lastEndTime = activities[i].end;
      }
    }
  }

  return selected;
}

int main() {
  // (시작 시간, 종료 시간) 형태의 활동 목록
  vector<Activity> activities = {
    {1, 4}, {3, 5}, {0, 6}, {5, 7}, {3, 9},
    {5, 9}, {6, 10}, {8, 11}, {8, 12}, {2, 14}, {12, 16}
  };

  vector<Activity> selected = activitySelection(activities);

  cout << "Number of selected activities: " << selected.size() << "\n";
  cout << "Selected activities: ";
  for (const auto& activity : selected)
    cout << activity << " ";
  cout << "\n";

  return 0;
}
```

<br>

### 회의실 배정 문제
- 목표: 한 회의실에서 최대한 많은 회의를 진행
- 방식: 회의들을 종료 시간 기준으로 정렬한 후, 겹치지 않게 선택

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Meeting {
  int start;
  int end;

  friend ostream& operator<<(ostream& os, const Meeting& meeting) {
    os << "(" << meeting.start << ", " << meeting.end << ")";
    return os;
  }
};

vector<Meeting> meetingRoomScheduling(vector<Meeting>& meetings) {
  // 종료 시간 기준으로 정렬
  sort(meetings.begin(), meetings.end(),
    [](const Meeting& a, const Meeting& b) {
      if (a.end == b.end) return a.start < b.start; // 종료 시간이 같으면 시작 시간 빠른 순
        return a.end < b.end;
    });

  vector<Meeting> scheduled;

  // 첫 번째 회의 선택
  if (!meetings.empty()) {
    scheduled.push_back(meetings[0]);
    int lastEndTime = meetings[0].end;

    // 나머지 회의들 중에서 선택
    for (size_t i = 1; i < meetings.size(); i++) {
      if (meetings[i].start >= lastEndTime) {
          scheduled.push_back(meetings[i]);
          lastEndTime = meetings[i].end;
      }
    }
  }

  return scheduled;
}

int main() {
  // (시작 시간, 종료 시간) 형태의 회의 목록
  vector<Meeting> meetings = {
    {1, 3}, {2, 4}, {3, 5}, {4, 6}, {5, 7}
  };

  vector<Meeting> scheduled = meetingRoomScheduling(meetings);

  cout << "Number of scheduled meetings: " << scheduled.size() << "\n";
  cout << "Scheduled meetings: ";
  for (const auto& meeting : scheduled)
    cout << meeting << " ";
  cout << "\n";

  return 0;
}
```

<br>

### 최소 신장 트리 (Kruskal 알고리듬)
- 목표: 가중치의 합이 최소인 트리 구성
- 조건: 사이클이 없어야 함
- 방식: 간선을 가중치 기준으로 정렬한 후, 사이클이 생기지 않도록 차례로 선택

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Edge {
  int src;
  int dest;
  int weight;

  friend ostream& operator<<(ostream& os, const Edge& edge) {
    os << "(" << edge.src << "-" << edge.dest << ", weight: " << edge.weight << ")";
    return os;
  }
};

// Kruskal 알고리듬을 이용한 최소 신장 트리 구현
class KruskalMST {
  private:
    // 유니온-파인드를 위한 부모 배열
    vector<int> parent;

    // 특정 원소가 속한 집합 찾기
    int find(int x) {
      if (parent[x] != x) parent[x] = find(parent[x]);  // 경로 압축
      return parent[x];
    }

    // 두 원소가 속한 집합 합치기
    void unionSets(int x, int y) {
      parent[find(x)] = find(y);
    }

  public:
    // 최소 신장 트리 구하기
    vector<Edge> findMST(vector<Edge>& edges, int vertices) {
      vector<Edge> result;

      // 간선을 가중치 기준으로 오름차순 정렬
      sort(edges.begin(), edges.end(),
        [](const Edge& a, const Edge& b) {
          return a.weight < b.weight;
        });

      // 부모 배열 초기화
      parent.resize(vertices);
      for (int i = 0; i < vertices; i++)
        parent[i] = i;  // 처음에는 자기 자신이 부모

      // 가중치가 작은 간선부터 선택
      for (const Edge& edge : edges) {
        int srcRoot = find(edge.src);
        int destRoot = find(edge.dest);

        // 사이클이 생기지 않는 경우에만 선택
        if (srcRoot != destRoot) {
          result.push_back(edge);
          unionSets(srcRoot, destRoot);

          // 최소 신장 트리는 (정점 수 - 1)개의 간선을 가짐
          if (result.size() == vertices - 1) break;
        }
      }

      return result;
    }
};

int main() {
  // 그래프 간선 정보 (src, dest, weight)
  vector<Edge> edges = {
    {0, 1, 10}, {0, 2, 6}, {0, 3, 5},
    {1, 3, 15}, {2, 3, 4}
  };
  int vertices = 4;  // 정점 수

  KruskalMST kruskal;
  vector<Edge> mst = kruskal.findMST(edges, vertices);

  cout << "Minimum Spanning Tree edges:" << "\n";
  int totalWeight = 0;
  for (const Edge& edge : mst) {
    cout << edge << "\n";
    totalWeight += edge.weight;
  }
  cout << "Total weight: " << totalWeight << "\n";

  return 0;
}
```

<br>

### 허프만 인코딩
- 목표: 가장 효율적인 이진 인코딩을 구성
- 방식: 가장 빈도 낮은 두 개의 노드를 반복적으로 합치는 방식으로 트리 구성

```cpp
#include <bits/stdc++.h>
using namespace std;

struct HuffmanNode {
  char ch;
  int freq;
  HuffmanNode *left, *right;

  HuffmanNode(char c, int f) : ch(c), freq(f), left(nullptr), right(nullptr) {}

  ~HuffmanNode() {
    delete left;
    delete right;
  }
};

// 우선순위 큐 비교를 위한 구조체
struct Compare {
  bool operator()(HuffmanNode* l, HuffmanNode* r) {
    return l->freq > r->freq; // 최소 힙
  }
};

void generateHuffmanCodes(HuffmanNode* root, string code, vector<pair<char, string>>& codes) {
  if (!root) return;

  // 리프 노드일 경우 코드 저장
  if (!root->left && !root->right)
    codes.push_back({root->ch, code});

  generateHuffmanCodes(root->left, code + "0", codes);
  generateHuffmanCodes(root->right, code + "1", codes);
}

vector<pair<char, string>> huffmanEncoding(vector<pair<char, int>>& freq) {
  // 최소 힙 우선순위 큐
  priority_queue<HuffmanNode*, vector<HuffmanNode*>, Compare> minHeap;

  // 빈도 데이터를 기반으로 노드 생성
  for (const auto& p : freq)
    minHeap.push(new HuffmanNode(p.first, p.second));

  // 허프만 트리 생성
  while (minHeap.size() > 1) {
    HuffmanNode *left = minHeap.top(); minHeap.pop();
    HuffmanNode *right = minHeap.top(); minHeap.pop();

    HuffmanNode *newNode = new HuffmanNode('$', left->freq + right->freq);
    newNode->left = left;
    newNode->right = right;

    minHeap.push(newNode);
  }

  // 허프만 코드 생성
  vector<pair<char, string>> codes;
  if (!minHeap.empty())
    generateHuffmanCodes(minHeap.top(), "", codes);

  delete minHeap.top();

  return codes;
}

int main() {
  // 문자와 빈도 정보
  vector<pair<char, int>> freq = {
    {'a', 45}, {'b', 13}, {'c', 12}, {'d', 16}, {'e', 9}, {'f', 5}
  };

  vector<pair<char, string>> codes = huffmanEncoding(freq);

  cout << "Huffman Codes:" << "\n";
  for (const auto& p : codes)
    cout << p.first << ": " << p.second << "\n";

  return 0;
}
```

<br>

## 반례: 그리디 알고리듬이 실패하는 경우

### ❌ 예시 1: 동전 문제 (비정형 단위)
- 동전 단위: `1원`, `3원`, `4원`
- 목표 금액: `6원`
- 그리디 선택: `4 + 1 + 1 = 3개`
- 최적해: `3 + 3 = 2개`

: 이 예시에서는 가장 큰 단위인 `4원`을 먼저 선택하게 되며, 이후 남은 금액 `2원`을 `1원`짜리 동전 두 개로 채우게 됩니다.

결과적으로 총 `3개`의 동전이 사용되지만, 실제로는 `3원`짜리 두 개만으로 `2개`의 동전으로 목표 금액을 만들 수 있습니다.

<br>
즉, 각 단계에서 최선처럼 보였던 선택이 전체 관점에서는 비효율적인 결과로 이어진 것입니다.

이러한 경우가 각 단계의 최선이 전체 최적해를 구성하지 못하는 상황,

**탐욕적 선택 속성(Greedy Choice Property)**이 성립하지 않는 경우에 해당합니다.

즉, 현재의 선택이 오히려 이후의 더 나은 선택을 방해하며, 최적의 결과로 이어지지 못하게 되는 것입니다.

<br>

### ❌ 예시 2: 배낭 문제 (0-1 Knapsack)
- 문제 설정: 여러 개의 물건이 있고, 총 무게 제한이 주어진 배낭에 일부 물건만을 선택해 담을 수 있음
- 조건: 물건은 쪼갤 수 없으며, 한 번 선택하면 통째로 담아야 함
- 전략: 가치 대비 무게 비율이 높은 순서대로 물건을 선택

예를 들어 다음과 같은 물건이 있다고 가정했을 때:

- `물건 A`: `무게 10`, `가치 60` (`비율 6`)
- `물건 B`: `무게 20`, `가치 100` (`비율 5`)
- `물건 C`: `무게 30`, `가치 120` (`비율 4`)

`배낭 용량: 50`

그리디 알고리듬은 비율이 높은 순서대로 `A → B → C` 순으로 물건을 살펴보고,

`A`와 `B`를 담는 것으로 결정을 내립니다. 이 경우 총 가치는 `160`입니다.

하지만 실제로는 `B`와 `C`를 선택하는 편이 더 나은 전략이며, 이 경우 총 가치 `220`을 얻을 수 있습니다.

즉, 비율이 높은 물건부터 선택하는 그리디 전략이 최적해를 보장하지 않는 경우입니다.

<br>
이처럼 하나의 선택이 이후 선택의 가능성에 영향을 주고, 물건을 쪼갤 수 없는 등의 제약 조건이 있는 경우에는

그리디 알고리듬보다는 **동적 계획법(Dynamic Programming)**을 사용하는 편이 더 적절합니다.

<br>

## 그리디와 다른 알고리듬 비교

| 분류 | 방식 | 특징 | 사용 조건 |
|------|------|------|-----------|
| 그리디 | 순간 최선만 선택 | 빠르고 간단 | 탐욕적 선택 속성 + 최적 부분 구조 |
| 동적 계획법 | 모든 경우를 고려하며 메모이제이션 | 느리지만 항상 최적 | 최적 부분 구조만 만족해도 가능 |
| 완전 탐색 | 모든 경우의 수를 전수조사 | 매우 느림 | 정답을 반드시 보장하지만 비효율적 |

<br>

## 구현 팁 및 시간 복잡도
- 대부분의 그리디 문제는 정렬 + 선형 탐색 구조
- 시간 복잡도는 일반적으로 **O(n log n)** (정렬) + **O(n)** (선택)으로 이루어짐
- 스케줄링 문제, 간선 선택 문제 등에서는 **정렬 기준이 문제의 핵심 조건**이 되는 경우가 많음

그리디 알고리듬을 적용하기 전에 항상 반례가 있는지 검토하는 것이 중요합니다

<br>

## 그리디 알고리듬 설계 단계
- 탐욕적 선택 속성 파악: 어떤 기준으로 '최선'을 판단할 것인지 정의
- 정렬 기준 결정: 대부분의 그리디 문제는 적절한 정렬이 핵심
- 선택 과정 구현: 정렬된 순서대로 조건을 만족하는 요소 선택
- 타당성 검증: 그리디 방식이 최적해를 보장하는지 수학적으로 증명하거나 반례 검토

<br>

## 알고리듬 적용 시 고려사항
그리디 알고리듬을 문제 해결에 적용할 때 다음 사항들을 체계적으로 검토하는 것이 중요합니다:

- 문제의 성질 분석: 해당 문제가 그리디 접근으로 해결 가능한지 확인
  - 탐욕적 선택 속성과 최적 부분 구조를 모두 만족하는지 검증
  - 간단한 반례를 통해 그리디 방식의 유효성 확인
- 최적 기준 선정: 각 단계에서 '최선'을 판단할 객관적 기준 설정
  - 종료 시간, 가중치, 비용 대비 효율 등 문제에 적합한 기준 선택
  - 해당 기준에 따라 요소들을 정렬하는 방식 결정
- 알고리듬 검증: 선택한 그리디 전략이 실제로 최적해를 보장하는지 증명
  - 수학적 귀납법, 반례 검토 등을 통한 알고리듬 정확성 확인
  - 시간 복잡도와 공간 복잡도 분석

<br>

## 마무리
그리디 알고리듬은 구현이 간단하고 실행 속도도 빠르기 때문에, 문제 상황이 잘 맞을 경우 매우 효과적인 선택이 될 수 있습니다.

특히 **탐욕적 선택 속성**과 **최적 부분 구조**를 모두 만족하는 문제에서는, 복잡한 알고리듬 없이도 간단한 로직만으로 최적해를 구할 수 있다는 큰 장점이 있습니다.

다만, 그리디 알고리듬이 항상 정답을 보장하는 것은 아니므로, **적용 전에 해당 문제 구조가 그리디 방식에 적합한지 충분히 분석하는 과정이 필요합니다.**

가능하다면 직접 반례를 만들어보며, 그리디 선택이 최적해로 이어지는지를 확인하는 과정이 중요합니다.

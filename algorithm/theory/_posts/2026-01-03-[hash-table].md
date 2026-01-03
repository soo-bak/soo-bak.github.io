---
layout: single
title: "해시 테이블(Hash Table)의 원리와 구현 - soo:bak"
date: "2026-01-03 04:00:00 +0900"
description: 키-값 쌍을 효율적으로 저장하고 검색하는 해시 테이블의 원리, 해시 함수, 충돌 처리 방법을 다룹니다
---

## 해시 테이블이란?

수천 개의 데이터에서 특정 값을 찾아야 한다고 가정해보겠습니다.

배열을 처음부터 끝까지 순회하며 찾는 방법은 $$O(n)$$의 시간이 걸립니다.

데이터가 많아질수록 검색 시간도 비례하여 증가하므로, 대량의 데이터를 다룰 때는 비효율적입니다.

<br>

**해시 테이블(Hash Table)**은 이러한 문제를 해결하는 자료구조입니다.

키(Key)를 값(Value)에 매핑하는 방식으로, **평균 $$O(1)$$ 시간**에 삽입, 삭제, 검색이 가능합니다.

<br>

해시 테이블의 동작 원리는 다음과 같습니다:

1. 키를 **해시 함수**에 입력하여 정수(해시값)를 얻습니다
2. 해시값을 배열의 인덱스로 사용하여 데이터를 저장합니다
3. 같은 키로 다시 접근하면 같은 위치를 바로 찾을 수 있습니다

```
키 "apple"  → 해시 함수 → 해시값 3 → 배열[3]에 저장
키 "banana" → 해시 함수 → 해시값 7 → 배열[7]에 저장
```

---

## 해시 함수

**해시 함수(Hash Function)**는 임의의 크기의 데이터를 고정된 크기의 값으로 변환하는 함수입니다.

<br>

좋은 해시 함수는 다음 조건을 만족해야 합니다:

- **결정적**: 같은 입력에는 항상 같은 출력을 반환
- **균등 분포**: 해시값이 배열 전체에 고르게 분포
- **빠른 계산**: 해시값 계산이 효율적
- **충돌 최소화**: 서로 다른 키가 같은 해시값을 갖는 경우가 적음

<br>

### 간단한 해시 함수 예시

문자열을 위한 간단한 해시 함수입니다.

```cpp
int simpleHash(const string& key, int tableSize) {
  int hash = 0;
  for (char c : key) {
    hash = (hash * 31 + c) % tableSize;
  }
  return hash;
}
```

각 문자의 아스키 값에 31을 곱하면서 누적하는 방식으로, 문자의 순서까지 반영됩니다.

<br>

정수 키의 경우 단순히 나머지 연산을 사용할 수 있습니다.

```cpp
int intHash(int key, int tableSize) {
  return key % tableSize;
}
```

---

## 충돌(Collision)과 해결 방법

서로 다른 키가 같은 해시값을 가지는 경우를 **충돌(Collision)**이라고 합니다.

```
"apple" → 해시값 3
"grape" → 해시값 3  (충돌!)
```

해시 함수가 아무리 좋아도 충돌은 피할 수 없습니다. 이를 해결하는 대표적인 방법이 있습니다.

<br>

### 체이닝 (Chaining)

같은 해시값을 가진 원소들을 **연결 리스트**로 연결하는 방식입니다.

```
배열[0]: NULL
배열[1]: NULL
배열[2]: NULL
배열[3]: "apple" → "grape" → NULL
배열[4]: NULL
...
```

<br>

```cpp
#include <bits/stdc++.h>
using namespace std;

class HashTableChaining {
private:
  int size;
  vector<list<pair<string, int>>> table;

  int hash(const string& key) {
    int h = 0;
    for (char c : key) {
      h = (h * 31 + c) % size;
    }
    return h;
  }

public:
  HashTableChaining(int s) : size(s), table(s) {}

  void insert(const string& key, int value) {
    int idx = hash(key);
    // 기존 키가 있으면 업데이트
    for (auto& p : table[idx]) {
      if (p.first == key) {
        p.second = value;
        return;
      }
    }
    table[idx].push_back({key, value});
  }

  int get(const string& key) {
    int idx = hash(key);
    for (const auto& p : table[idx]) {
      if (p.first == key) {
        return p.second;
      }
    }
    return -1;  // 키가 없음
  }

  void remove(const string& key) {
    int idx = hash(key);
    table[idx].remove_if([&](const pair<string, int>& p) {
      return p.first == key;
    });
  }
};
```

체이닝은 구현이 간단하고, 부하율이 1을 초과해도 동작합니다.

단, 연결 리스트 탐색으로 인해 캐시 효율이 낮을 수 있습니다.

<br>

### 개방 주소법 (Open Addressing)

충돌이 발생하면 **다른 빈 칸**을 찾아 저장하는 방식입니다.

추가 메모리 없이 테이블 내에서 해결하므로 캐시 효율이 좋습니다.

<br>

**선형 탐사 (Linear Probing)**

충돌 시 다음 칸을 순차적으로 확인합니다.

```cpp
class HashTableLinear {
private:
  int size;
  vector<pair<string, int>> table;
  vector<bool> occupied;

  int hash(const string& key) {
    int h = 0;
    for (char c : key) {
      h = (h * 31 + c) % size;
    }
    return h;
  }

public:
  HashTableLinear(int s) : size(s), table(s), occupied(s, false) {}

  void insert(const string& key, int value) {
    int idx = hash(key);
    int start = idx;

    while (occupied[idx]) {
      if (table[idx].first == key) {
        table[idx].second = value;  // 업데이트
        return;
      }
      idx = (idx + 1) % size;
      if (idx == start) return;  // 테이블 가득 참
    }

    table[idx] = {key, value};
    occupied[idx] = true;
  }

  int get(const string& key) {
    int idx = hash(key);
    int start = idx;

    while (occupied[idx]) {
      if (table[idx].first == key) {
        return table[idx].second;
      }
      idx = (idx + 1) % size;
      if (idx == start) break;
    }

    return -1;  // 키가 없음
  }
};
```

선형 탐사는 구현이 간단하지만, 데이터가 연속된 영역에 몰리는 **군집화(Clustering)** 문제가 발생할 수 있습니다.

<br>

**이차 탐사 (Quadratic Probing)**

군집화 문제를 줄이기 위해 $$i^2$$씩 점프합니다.

```cpp
int probe(int idx, int i, int size) {
  return (idx + i * i) % size;
}
```

<br>

**이중 해싱 (Double Hashing)**

두 번째 해시 함수로 점프 크기를 결정하여 더 균등하게 분포시킵니다.

```cpp
int hash2(const string& key, int size) {
  int h = 0;
  for (char c : key) {
    h = (h * 17 + c) % size;
  }
  return h == 0 ? 1 : h;  // 0이면 1로 대체
}

int probe(int idx, int i, const string& key, int size) {
  return (idx + i * hash2(key, size)) % size;
}
```

---

## 시간 복잡도

해시 테이블의 시간 복잡도는 평균적으로 $$O(1)$$입니다.

삽입, 검색, 삭제 모두 해시값을 계산하고 해당 위치에 접근하면 되기 때문입니다.

<br>

하지만 최악의 경우, 모든 키가 같은 해시값을 가진다면 $$O(n)$$이 됩니다.

이는 모든 데이터가 하나의 연결 리스트에 저장되어 순차 탐색이 필요해지기 때문입니다.

<br>

공간 복잡도는 $$O(n)$$입니다.

---

## 부하율 (Load Factor)

**부하율(Load Factor)**은 테이블이 얼마나 채워졌는지를 나타내는 지표입니다.

$$
\text{부하율} = \frac{\text{저장된 원소 수}}{\text{테이블 크기}}
$$

<br>

부하율이 높아지면 충돌 확률이 증가하고 성능이 저하됩니다.

일반적으로 부하율이 0.7~0.8을 초과하면 **테이블 크기 조정**을 수행합니다.

```cpp
void resize() {
  int newSize = size * 2;
  vector<list<pair<string, int>>> newTable(newSize);

  for (auto& bucket : table) {
    for (auto& p : bucket) {
      int newIdx = hash(p.first, newSize);
      newTable[newIdx].push_back(p);
    }
  }

  table = move(newTable);
  size = newSize;
}
```

크기 조정 시 모든 원소를 새로운 테이블에 다시 삽입해야 하므로 $$O(n)$$의 시간이 소요됩니다.

하지만 크기 조정은 드물게 발생하므로, 분할 상환 분석(Amortized Analysis)으로 보면 여전히 평균 $$O(1)$$입니다.

---

## C++ STL의 해시 테이블

C++ STL은 `unordered_map`과 `unordered_set`을 제공합니다.

내부적으로 해시 테이블을 사용하며, 평균 $$O(1)$$ 시간에 동작합니다.

<br>

### unordered_map 사용

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  unordered_map<string, int> scores;

  // 삽입
  scores["Alice"] = 95;
  scores["Bob"] = 87;
  scores["Charlie"] = 92;

  // 검색
  cout << scores["Alice"] << "\n";  // 95

  // 존재 여부 확인
  if (scores.count("Bob")) {
    cout << "Bob exists\n";
  }

  // 순회
  for (auto& [name, score] : scores) {
    cout << name << ": " << score << "\n";
  }

  // 삭제
  scores.erase("Bob");

  return 0;
}
```

> 참고: `unordered_map`은 순서를 보장하지 않습니다. 순서가 필요하다면 `map`을 사용해야 합니다.

<br>

### unordered_set 사용

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  unordered_set<int> visited;

  visited.insert(1);
  visited.insert(5);
  visited.insert(3);

  if (visited.count(5)) {
    cout << "5 is visited\n";
  }

  return 0;
}
```

---

## 해시 테이블의 활용

### 빈도 수 세기

문자열에서 각 문자가 몇 번 등장하는지 셀 수 있습니다.

```cpp
unordered_map<char, int> freq;
string s = "hello";
for (char c : s) {
  freq[c]++;
}
// freq: {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

<br>

### 중복 확인

배열에 중복된 값이 있는지 $$O(n)$$ 시간에 확인할 수 있습니다.

```cpp
bool hasDuplicate(vector<int>& nums) {
  unordered_set<int> seen;
  for (int n : nums) {
    if (seen.count(n)) return true;
    seen.insert(n);
  }
  return false;
}
```

<br>

### 두 수의 합 (Two Sum)

배열에서 합이 target이 되는 두 원소의 인덱스를 찾는 문제입니다.

```cpp
vector<int> twoSum(vector<int>& nums, int target) {
  unordered_map<int, int> seen;  // 값 → 인덱스

  for (int i = 0; i < nums.size(); i++) {
    int complement = target - nums[i];
    if (seen.count(complement)) {
      return {seen[complement], i};
    }
    seen[nums[i]] = i;
  }

  return {};
}
```

각 원소를 순회하면서 필요한 값이 이미 등장했는지 해시 테이블로 확인합니다.

$$O(n^2)$$ 이중 반복문 대신 $$O(n)$$ 시간에 해결할 수 있습니다.

<br>

### 그룹화

특정 기준에 따라 데이터를 그룹화할 수 있습니다.

```cpp
unordered_map<int, vector<string>> byLength;
vector<string> words = {"a", "bc", "def", "ab"};

for (auto& w : words) {
  byLength[w.length()].push_back(w);
}
// byLength: {1: ["a"], 2: ["bc", "ab"], 3: ["def"]}
```

---

## 마무리

해시 테이블은 키를 해시 함수로 변환하여 배열 인덱스로 사용함으로써, 평균 $$O(1)$$ 시간에 데이터를 저장하고 검색하는 자료구조입니다.

<br>

충돌이 발생할 수 있으므로 체이닝이나 개방 주소법으로 이를 처리해야 하며, 부하율 관리를 통해 성능을 유지합니다.

<br>

빈도 계산, 중복 확인, 빠른 검색이 필요한 문제에서 해시 테이블은 매우 유용하게 활용됩니다.

C++에서는 `unordered_map`과 `unordered_set`을 통해 간편하게 사용할 수 있습니다.

<br>

**관련 글**:
- [스택과 큐(Stack and Queue)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/stack-queue/)

<br>

**관련 문제**:
- [[백준 1920] 수 찾기](https://soo-bak.github.io/algorithm/boj/FindNumber-85/)
- [[백준 10816] 숫자 카드 2](https://soo-bak.github.io/algorithm/boj/NumberCard2-90/)

---
layout: single
title: "해시 테이블(Hash Table)의 원리와 구현 - soo:bak"
date: "2026-01-03 04:00:00 +0900"
description: 키-값 쌍을 효율적으로 저장하고 검색하는 해시 테이블의 원리, 해시 함수, 충돌 처리 방법을 다룹니다
---

## 해시 테이블이란?

**해시 테이블(Hash Table)**은 키(Key)를 값(Value)에 매핑하는 자료구조로, **평균 $$O(1)$$ 시간**에 삽입, 삭제, 검색이 가능합니다.

<br>

**해시 테이블의 핵심 아이디어**:

1. 키를 **해시 함수**에 입력하여 정수(해시값)를 얻음
2. 해시값을 배열의 인덱스로 사용하여 데이터 저장
3. 같은 키로 다시 접근하면 같은 위치를 바로 찾음

<br>

```
키 "apple" → 해시 함수 → 해시값 3 → 배열[3]에 저장
키 "banana" → 해시 함수 → 해시값 7 → 배열[7]에 저장
```

<br>

## 해시 함수란?

**해시 함수(Hash Function)**는 임의의 크기의 데이터를 고정된 크기의 값으로 변환하는 함수입니다.

<br>

**좋은 해시 함수의 조건**:

1. **결정적**: 같은 입력에는 항상 같은 출력
2. **균등 분포**: 해시값이 배열 전체에 고르게 분포
3. **빠른 계산**: 해시값 계산이 효율적
4. **충돌 최소화**: 서로 다른 키가 같은 해시값을 갖는 경우가 적음

<br>

### 간단한 해시 함수 예시

```cpp
// 문자열을 위한 간단한 해시 함수
int simpleHash(const string& key, int tableSize) {
  int hash = 0;
  for (char c : key) {
    hash = (hash * 31 + c) % tableSize;
  }
  return hash;
}
```

<br>

### 정수 키를 위한 해시 함수

```cpp
int intHash(int key, int tableSize) {
  return key % tableSize;
}
```

<br>

## 충돌(Collision)과 해결 방법

서로 다른 키가 같은 해시값을 가지는 경우를 **충돌(Collision)**이라고 합니다.

<br>

**예시**:
```
"apple" → 해시값 3
"grape" → 해시값 3  (충돌!)
```

<br>

충돌을 해결하는 대표적인 방법 두 가지:

<br>

### 1. 체이닝 (Chaining)

같은 해시값을 가진 원소들을 **연결 리스트**로 연결합니다.

```
배열[0]: NULL
배열[1]: NULL
배열[2]: NULL
배열[3]: "apple" → "grape" → NULL
배열[4]: NULL
...
```

<br>

**체이닝 구현**

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

<br>

### 2. 개방 주소법 (Open Addressing)

충돌이 발생하면 **다른 빈 슬롯**을 찾아 저장합니다.

<br>

**선형 탐사 (Linear Probing)**

충돌 시 다음 슬롯을 순차적으로 확인합니다.

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

<br>

**이차 탐사 (Quadratic Probing)**

선형 탐사의 군집화 문제를 해결합니다.

```cpp
int probe(int idx, int i, int size) {
  return (idx + i * i) % size;  // i^2씩 점프
}
```

<br>

**이중 해싱 (Double Hashing)**

두 번째 해시 함수로 점프 크기를 결정합니다.

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

<br>

## 체이닝 vs 개방 주소법

<br>

| 특성 | 체이닝 | 개방 주소법 |
|------|--------|------------|
| 구현 복잡도 | 간단 | 복잡 |
| 메모리 사용 | 포인터 오버헤드 | 테이블만 사용 |
| 캐시 효율 | 낮음 | 높음 |
| 삭제 연산 | 간단 | 복잡 (tombstone 필요) |
| 부하율 > 1 | 가능 | 불가능 |

<br>

## 시간 복잡도

<br>

| 연산 | 평균 | 최악 |
|------|------|------|
| 삽입 | $$O(1)$$ | $$O(n)$$ |
| 검색 | $$O(1)$$ | $$O(n)$$ |
| 삭제 | $$O(1)$$ | $$O(n)$$ |

<br>

최악의 경우는 모든 키가 같은 해시값을 가질 때 발생합니다.

**공간 복잡도**: $$O(n)$$

<br>

## 부하율 (Load Factor)

**부하율** = 저장된 원소 수 / 테이블 크기

<br>

부하율이 높아지면:
- 충돌 확률 증가
- 성능 저하

<br>

일반적으로 부하율이 0.7~0.8을 초과하면 **리사이징(Resizing)**을 수행합니다.

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

<br>

## C++ STL의 해시 테이블

C++ STL은 `unordered_map`과 `unordered_set`을 제공합니다.

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

<br>

## 해시 테이블의 활용

<br>

**1. 빈도 수 세기**

```cpp
unordered_map<char, int> freq;
string s = "hello";
for (char c : s) {
  freq[c]++;
}
// freq: {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

<br>

**2. 중복 확인**

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

**3. 두 수의 합 (Two Sum)**

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

<br>

**4. 그룹화**

```cpp
unordered_map<int, vector<string>> byLength;
vector<string> words = {"a", "bc", "def", "ab"};

for (auto& w : words) {
  byLength[w.length()].push_back(w);
}
// byLength: {1: ["a"], 2: ["bc", "ab"], 3: ["def"]}
```

<br>

## 마무리

해시 테이블은 평균 $$O(1)$$ 시간에 삽입, 삭제, 검색이 가능한 강력한 자료구조입니다.

<br>

**핵심 포인트**
- **해시 함수**: 키를 배열 인덱스로 변환
- **충돌 처리**: 체이닝 또는 개방 주소법
- **시간 복잡도**: 평균 $$O(1)$$, 최악 $$O(n)$$
- **부하율 관리**: 성능 유지를 위한 리사이징

<br>

해시 테이블은 빈도 계산, 중복 확인, 빠른 검색이 필요한 다양한 문제에서 핵심적으로 활용됩니다.

<br>

### 관련 글
- [스택과 큐(Stack and Queue)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/stack-queue/)

<br>

### 관련 문제
- [[백준 1920] 수 찾기](https://www.acmicpc.net/problem/1920)
- [[백준 10816] 숫자 카드 2](https://www.acmicpc.net/problem/10816)


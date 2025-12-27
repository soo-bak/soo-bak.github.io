---
layout: single
title: "완전탐색(Brute Force)의 원리와 구현 - soo:bak"
date: "2025-12-27 01:10:00 +0900"
description: 완전탐색의 개념과 다양한 구현 방법, 시간 복잡도 분석, 최적화 기법까지 브루트포스 알고리즘을 상세히 설명합니다.
---

## 완전탐색이란?

**완전탐색(Brute Force)** 은 가능한 모든 경우의 수를 하나씩 검사하여 정답을 찾는 알고리즘입니다.

<br>
"무식하게 풀기"라고도 불리지만, 가장 확실하고 직관적인 문제 해결 방법입니다.

<br>
완전탐색의 핵심은 **모든 가능성을 빠짐없이 탐색**하는 것입니다.

정답이 존재한다면 반드시 찾을 수 있습니다.

<br>

---

<br>

## 완전탐색을 사용하는 경우

완전탐색은 다음과 같은 상황에서 적합합니다:

<br>

**1. 입력 크기가 작은 경우**

경우의 수가 적으면 모두 탐색해도 시간 내에 해결됩니다.

<br>

**2. 최적화 알고리즘을 모르는 경우**

일단 완전탐색으로 정답을 구한 뒤, 필요하면 최적화합니다.

<br>

**3. 정확한 답이 필요한 경우**

근사치가 아닌 정확한 최적해가 필요할 때 사용합니다.

<br>

---

<br>

## 완전탐색의 구현 방법

### 1. 반복문을 이용한 탐색

가장 단순한 형태로, 중첩 반복문을 사용합니다.

<br>

**예시: 배열에서 합이 K인 두 수 찾기**

```cpp
#include <bits/stdc++.h>
using namespace std;

pair<int, int> findTwoSum(vector<int>& arr, int k) {
    int n = arr.size();
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (arr[i] + arr[j] == k)
                return {i, j};
        }
    }
    return {-1, -1};
}
```

<br>
시간 복잡도: **O(n²)**

<br>

### 2. 재귀를 이용한 탐색

선택의 연속인 문제에서 재귀를 활용합니다.

<br>

**예시: 부분집합 생성**

```cpp
#include <bits/stdc++.h>
using namespace std;

void generateSubsets(vector<int>& arr, int idx, vector<int>& current) {
    if (idx == arr.size()) {
        // current가 하나의 부분집합
        for (int x : current) cout << x << " ";
        cout << "\n";
        return;
    }

    // arr[idx]를 포함하지 않는 경우
    generateSubsets(arr, idx + 1, current);

    // arr[idx]를 포함하는 경우
    current.push_back(arr[idx]);
    generateSubsets(arr, idx + 1, current);
    current.pop_back();
}
```

<br>
시간 복잡도: **O(2ⁿ)** (부분집합의 개수)

<br>

### 3. 순열과 조합

순서가 중요한 경우 순열, 그렇지 않은 경우 조합을 생성합니다.

<br>

**순열 생성 (next_permutation)**

```cpp
#include <bits/stdc++.h>
using namespace std;

void printAllPermutations(vector<int>& arr) {
    sort(arr.begin(), arr.end());
    do {
        for (int x : arr) cout << x << " ";
        cout << "\n";
    } while (next_permutation(arr.begin(), arr.end()));
}
```

<br>
n개 원소의 순열: **n!** 개

<br>

### 4. 비트마스크를 이용한 탐색

집합의 부분집합을 정수로 표현하여 탐색합니다.

<br>

**예시: 부분집합의 합**

```cpp
#include <bits/stdc++.h>
using namespace std;

int countSubsetsWithSum(vector<int>& arr, int target) {
    int n = arr.size();
    int count = 0;

    for (int mask = 0; mask < (1 << n); mask++) {
        int sum = 0;
        for (int i = 0; i < n; i++) {
            if (mask & (1 << i))
                sum += arr[i];
        }
        if (sum == target) count++;
    }
    return count;
}
```

<br>
시간 복잡도: **O(2ⁿ × n)**

<br>

---

<br>

## 시간 복잡도 추정

완전탐색의 실행 시간을 미리 예측하는 것이 중요합니다.

<br>

| 경우의 수 | 대략적인 연산 횟수 | 실행 가능 여부 (1초 기준) |
|----------|------------------|------------------------|
| 10! | 약 360만 | ✅ 가능 |
| 2²⁰ | 약 100만 | ✅ 가능 |
| 2²⁵ | 약 3300만 | ⚠️ 경계선 |
| 2³⁰ | 약 10억 | ❌ 어려움 |
| 15! | 약 1조 | ❌ 불가능 |

<br>
일반적으로 **1초에 약 1억 번**의 단순 연산이 가능하다고 추정합니다.

<br>

---

<br>

## 완전탐색의 최적화

### 1. 가지치기 (Pruning)

탐색 도중 **불가능한 경우를 조기에 제외**합니다.

<br>

```cpp
void search(int idx, int currentSum, int target) {
    // 가지치기: 이미 목표를 초과하면 더 탐색할 필요 없음
    if (currentSum > target) return;

    // 가지치기: 남은 모든 원소를 더해도 목표에 못 미치면 종료
    if (currentSum + remainingSum < target) return;

    // ... 탐색 계속
}
```

<br>

### 2. 메모이제이션

같은 상태를 여러 번 방문하는 경우, 결과를 저장하여 재사용합니다.

<br>
이것이 **동적 계획법(DP)** 으로 발전합니다.

<br>

### 3. 탐색 순서 최적화

**가능성이 높은 경우를 먼저 탐색**하면 정답을 빨리 찾을 수 있습니다.

<br>

---

<br>

## 완전탐색 문제 해결 전략

**1단계: 경우의 수 파악**

문제에서 탐색해야 할 전체 경우의 수를 계산합니다.

<br>

**2단계: 시간 복잡도 추정**

계산한 경우의 수가 제한 시간 내에 탐색 가능한지 확인합니다.

<br>

**3단계: 탐색 방법 선택**

반복문, 재귀, 비트마스크 중 적합한 방법을 선택합니다.

<br>

**4단계: 가지치기 적용**

불필요한 탐색을 줄일 수 있는 조건을 추가합니다.

<br>

---

<br>

## 관련 문제 유형

완전탐색은 다음과 같은 문제에서 활용됩니다:

- 조합 최적화 (배낭 문제의 작은 입력)
- 게임 이론 (가능한 모든 수 탐색)
- 암호 해독 (가능한 모든 키 시도)
- 경로 탐색 (모든 경로 열거)
- 스도쿠, 퍼즐 해결

<br>


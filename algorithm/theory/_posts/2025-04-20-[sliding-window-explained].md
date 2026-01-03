---
layout: single
title: "슬라이딩 윈도우(Sliding Window)의 이해와 구현 - soo:bak"
date: "2025-04-20 23:33:00 +0900"
description: 슬라이딩 윈도우 알고리듬의 원리와 구현 방법을 다루고, 연속 구간 문제를 해결하는 사례를 설명한 글
tags:
  - 슬라이딩윈도우
  - 투포인터
---

## 슬라이딩 윈도우란?

**슬라이딩 윈도우(Sliding Window)**는 배열이나 문자열에서 **연속된 구간**을 설정하고,<br>
<br>
이 구간을 이동하며 조건을 만족하는 결과를 찾는 알고리듬 기법입니다. <br>
<br>
즉, 두 개의 포인터(`start`, `end`)를 사용해 구간의 시작과 끝을 관리하며, 구간을 **확장**하거나 **축소**해 문제를 해결합니다. <br><br>

**투 포인터**의 한 형태로, 포인터가 같은 방향으로 이동하는 패턴에 속하며, 연속된 데이터 탐색에 특화되어 있습니다. <br><br>

> 참고 : [투 포인터 알고리듬(Two Pointer Algorithm)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/two-pointer-explained/)

예를 들어, <br>
- 배열에서 특정 합을 만족하는 가장 긴 연속 구간을 구하는 경우.
- 문자열에서 특정 문자가 포함된 가장 짧은 부분 문자열을 찾는 경우.

---

## 슬라이딩 윈도우의 원리

슬라이딩 윈도우는 **고정 크기** 또는 **가변 크기**의 구간을 설정합니다.<br>
<br>
두 포인터가 구간을 정의하며, 조건에 따라 윈도우를 이동하거나 크기를 조정합니다. <br>

1. **고정 크기 윈도우** <br>
   - 구간의 길이가 고정되어 있음.
   - `end`와 `start`가 고정된 간격을 유지하며 이동.
   - 예: 길이 `k`인 구간의 `최대 합` 구하기.

2. **가변 크기 윈도우** <br>
   - 구간의 크기가 조건에 따라 변함.
   - `end`를 늘려 구간을 확장하고, 필요 시 `start`를 이동해 축소.
   - 예: `특정 조건`을 만족하는 `최소 또는 최대 구간` 찾기.

---

## 알고리듬적 접근

슬라이딩 윈도우는 투 포인터 알고리듬의 일종이므로, 투 포인터 알고리듬과 같이 **효율성**이 핵심입니다.<br>
<br>
완전 탐색으로는 $$O(n^2)$$ 이상이 걸릴 수 있는 문제들에 대해서, 슬라이딩 윈도우는 $$O(n)$$으로 문제를 해결합니다. <br>
<br>

### 고정 크기 윈도우 예시
<br>
문제: 배열에서 길이 `k`인 연속 구간의 최대 합을 구하기. <br>
예: `[4, 2, 1, 7, 8]`, `k = 3` → `[1, 7, 8]`의 합 `16`

1. 초기 윈도우 설정:
   - 첫 `k`개 원소의 합 계산.
   - 예: `[4, 2, 1]` → 합 = `7`
2. 윈도우 이동:
   - `end`와 `start`를 `1`씩 증가.
   - 새 원소 추가, 이전 원소 제거.
   - 예: `[2, 1, 7]` → 합 = `10`, `[1, 7, 8]` → 합 = `16`
3. 최대 합 갱신:
   - 각 윈도우의 합을 비교.


<br>
### C++ 코드 구현 (고정 크기 윈도우)

```cpp
#include <bits/stdc++.h>

int maxSumFixedWindow(vector<int>& arr, int k) {
  int n = arr.size();
  if (n < k) return 0;

  int currentSum = 0;
  for (int i = 0; i < k; i++)
    currentSum += arr[i];

  int maxSum = currentSum;
  for (int i = k; i < n; i++) {
    currentSum += arr[i] - arr[i - k];
    maxSum = max(maxSum, currentSum);
  }

  return maxSum;
}
```

---
<br>
### 가변 크기 윈도우 예시
<br>
문제: 문자열에서 `k`개의 특정 문자를 포함하는 `가장 짧은 부분 문자열의 길이`를 구하기. <br>
예: `"ADOBECODEBANC"`, `k = 4` (문자 `A`, `B`, `C`, `D`), 결과: `"BANC"` (길이 = `4`).

1. 초기화:
   - `start = 0`, `end = 0`, 문자 빈도를 추적하는 해시맵.
2. 윈도우 확장:
   - `end`를 이동하며 문자 추가, 필요한 문자 개수 확인.
3. 윈도우 축소:
   - 조건 만족 시 `start`를 이동해 최소 길이 갱신.
4. 반복:
   - `end`가 문자열 끝에 도달할 때까지.


<br>
### C++ 코드 구현 (가변 크기 윈도우)

```cpp
#include <bits/stdc++.h>

string minWindow(string s, string t) {
  unordered_map<char, int> need, window;
  for (char c : t) need[c]++;

  int required = need.size(), formed = 0;
  int start = 0, end = 0, minLen = INT_MAX, minStart = 0;

  while (end < s.size()) {
    window[s[end]]++;
    if (need.count(s[end]) && window[s[end]] == need[s[end]]) formed++;

    while (formed == required && start <= end) {
      if (end - start + 1 < minLen) {
        minLen = end - start + 1;
        minStart = start;
      }
      window[s[start]]--;
      if (need.count(s[start]) && window[s[start]] < need[s[start]]) formed--;
      start++;
   }
   end++;
  }

  return minLen == INT_MAX ? "" : s.substr(minStart, minLen);
}
```

<br>
이처럼 슬라이딩 윈도우는 연속 구간 문제를 간단히 해결합니다.

---

## 시간 복잡도

1. **고정 크기 윈도우**:
   - 배열을 한 번 순회: $$O(n)$$.
   - 초기 합 계산: $$O(k)$$, 이동: $$O(n-k)$$.

2. **가변 크기 윈도우**:
   - 각 포인터가 최대 $$n$$번 이동: $$O(n)$$.
   - 해시맵 사용 시 추가 비용 발생 가능.

---

## 활용 예시

- **구간 합 문제**: 고정 크기 윈도우로 최대/최소 합 계산.
- **문자열 패턴**: 특정 문자를 포함하는 최소 구간 탐색.

알고리듬 문제 해결 뿐만 아니라, 로그 데이터에서 특정 패턴이 포함된 연속 구간을 찾는 경우, 특정 시간 내의 이벤트 수를 집계하는 경우 등의 데이터 분석에도 유용합니다.

---

## 주의사항

1. **윈도우 크기**:
   - 고정/가변 여부를 상황에 따라 확인.
2. **조건 관리**:
   - 윈도우 조건(합, 문자 개수 등)을 정확히 처리.
3. **경계 처리**:
   - 포인터가 범위를 벗어나지 않도록 주의.

---

## 마무리

슬라이딩 윈도우는 연속 구간을 효율적으로 탐색하는 간단한 기법입니다. <br>
<br>
$$O(n)$$의 시간 복잡도로 빠르게 동작하며, 배열과 문자열 문제를 간단하게 해결합니다. <br>
<br>
또한, 구현이 직관적이어서 다양한 문제에 쉽게 적용할 수 있습니다. <br>
<br>

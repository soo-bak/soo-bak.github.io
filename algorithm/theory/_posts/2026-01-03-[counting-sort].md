---
layout: single
title: "계수 정렬(Counting Sort)의 원리와 구현 - soo:bak"
date: "2026-01-03 09:00:00 +0900"
description: 비교 없이 원소의 개수를 세어 정렬하는 계수 정렬 알고리듬의 원리, 구현 방법, 시간 복잡도를 다룹니다
---

## 계수 정렬이란?

**계수 정렬(Counting Sort)**은 원소들을 비교하지 않고, 각 원소의 **등장 횟수**를 세어 정렬하는 알고리듬입니다.

비교 기반 정렬의 하한인 $$O(n \log n)$$을 깨고, **$$O(n + k)$$** 시간에 정렬할 수 있습니다.

여기서 $$k$$는 원소의 최댓값입니다.

다만, 원소가 **정수**여야 하고, 원소의 범위가 **제한적**이어야 합니다. $$k$$가 너무 크면 비효율적입니다.

> 참고: [안정 정렬(Stable Sort)의 개념과 중요성 - soo:bak](https://soo-bak.github.io/algorithm/theory/stable-sort/)

---

## 계수 정렬의 원리

배열 `[4, 2, 2, 8, 3, 3, 1]`을 정렬하는 과정입니다:

<br>

### 1단계: 개수 세기

각 값의 등장 횟수를 셉니다:

```
값:    0  1  2  3  4  5  6  7  8
개수:  0  1  2  2  1  0  0  0  1
```

<br>

### 2단계: 누적 합 계산

개수 배열의 누적 합을 구합니다:

```
값:    0  1  2  3  4  5  6  7  8
누적:  0  1  3  5  6  6  6  6  7
```

누적 합은 "해당 값 이하의 원소가 몇 개인지"를 나타냅니다.

<br>

### 3단계: 출력 배열 생성

원본 배열을 역순으로 순회하며 출력 배열에 배치합니다:

- 각 원소를 누적 합이 가리키는 위치에 배치
- 배치 후 누적 합을 1 감소

역순으로 순회하는 이유는 같은 값을 가진 원소들의 상대적 순서를 유지하기 위해서입니다. 이렇게 하면 **안정 정렬(Stable Sort)**이 됩니다.

<br>

**결과**: `[1, 2, 2, 3, 3, 4, 8]`

---

## 구현

### 기본 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

void countingSort(vector<int>& arr) {
  if (arr.empty()) return;

  int maxVal = *max_element(arr.begin(), arr.end());
  int minVal = *min_element(arr.begin(), arr.end());
  int range = maxVal - minVal + 1;

  vector<int> count(range, 0);
  vector<int> output(arr.size());

  // 1단계: 개수 세기
  for (int num : arr) {
    count[num - minVal]++;
  }

  // 2단계: 누적 합 계산
  for (int i = 1; i < range; i++) {
    count[i] += count[i - 1];
  }

  // 3단계: 출력 배열 생성 (역순으로 순회 - 안정성 보장)
  for (int i = arr.size() - 1; i >= 0; i--) {
    int idx = count[arr[i] - minVal] - 1;
    output[idx] = arr[i];
    count[arr[i] - minVal]--;
  }

  arr = output;
}

int main() {
  vector<int> arr = {4, 2, 2, 8, 3, 3, 1};

  countingSort(arr);

  for (int x : arr) cout << x << " ";
  cout << "\n";
  // 출력: 1 2 2 3 3 4 8

  return 0;
}
```

<br>

### 간단한 버전 (안정성 불필요 시)

안정 정렬이 필요하지 않은 경우, 누적 합 계산 없이 더 간단하게 구현할 수 있습니다.

```cpp
void countingSortSimple(vector<int>& arr) {
  if (arr.empty()) return;

  int maxVal = *max_element(arr.begin(), arr.end());
  vector<int> count(maxVal + 1, 0);

  // 개수 세기
  for (int num : arr) {
    count[num]++;
  }

  // 정렬된 배열 생성
  int idx = 0;
  for (int i = 0; i <= maxVal; i++) {
    while (count[i]-- > 0) {
      arr[idx++] = i;
    }
  }
}
```

---

## 시간 복잡도

계수 정렬의 시간 복잡도는 $$O(n + k)$$입니다.

<br>

**개수 세기**: $$O(n)$$
- 배열을 한 번 순회하며 각 원소의 개수를 셉니다.

**누적 합 계산**: $$O(k)$$
- 범위 $$k$$만큼 순회하며 누적 합을 계산합니다.

**출력 배열 생성**: $$O(n)$$
- 배열을 역순으로 순회하며 결과 배열을 생성합니다.

<br>

**공간 복잡도**: $$O(n + k)$$
- 개수 배열: $$O(k)$$
- 출력 배열: $$O(n)$$

> 참고: [제자리 정렬(In-place Sort)의 개념과 중요성 - soo:bak](https://soo-bak.github.io/algorithm/theory/in-place-sort/)

---

## 계수 정렬의 특징

<br>

### 장점

- **선형 시간**: $$O(n + k)$$로 매우 빠름
- **안정 정렬**: 같은 값의 상대적 순서 유지
- **단순한 구현**: 비교 연산 없이 구현 가능

<br>

### 단점

- **정수 전용**: 실수나 문자열에는 직접 적용 불가
- **메모리 사용**: 범위가 크면 메모리 낭비
- **범위 제한**: $$k$$가 $$n$$보다 훨씬 크면 비효율적

<br>

### 적용 조건

계수 정렬이 효율적인 경우는 $$k = O(n)$$일 때입니다. 즉, 범위가 원소 수에 비례할 때 효과적입니다.

예를 들어 나이(0~150), 성적(0~100), ASCII 문자(0~127) 같은 경우가 적합합니다.

---

## 계수 정렬의 활용

<br>

### 문자 빈도 정렬

```cpp
string sortByFrequency(string s) {
  vector<int> count(256, 0);

  for (char c : s) {
    count[c]++;
  }

  string result;
  for (int i = 0; i < 256; i++) {
    result += string(count[i], (char)i);
  }

  return result;
}
```

<br>

### 성적 정렬

성적(0~100)처럼 범위가 제한된 정수 정렬에 적합합니다.

<br>

### 기수 정렬의 보조 정렬

기수 정렬에서 각 자릿수 정렬에 계수 정렬을 사용합니다.

---

## 마무리

계수 정렬은 정수 범위가 제한적일 때 $$O(n + k)$$ 시간에 정렬하는 효율적인 알고리듬입니다.

<br>

원소를 비교하지 않고 개수를 세어 정렬하는 방식으로, 비교 기반 정렬의 하한인 $$O(n \log n)$$을 깰 수 있습니다.

<br>

역순 순회를 통해 안정 정렬을 보장하며, 범위가 작은 정수 데이터에서는 비교 기반 정렬보다 훨씬 빠르게 정렬할 수 있습니다.

<br>

**관련 글**:
- [안정 정렬(Stable Sort)의 개념과 중요성 - soo:bak](https://soo-bak.github.io/algorithm/theory/stable-sort/)
- [빠른 정렬(Quick Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/quick-sort/)
- [병합 정렬(Merge Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/merge-sort/)

<br>

**관련 문제**:
- [[백준 10989] 수 정렬하기 3](https://www.acmicpc.net/problem/10989)

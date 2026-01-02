---
layout: single
title: "선형 탐색(Linear Search)의 원리와 구현 - soo:bak"
date: "2026-01-03 01:00:00 +0900"
description: 배열에서 원하는 값을 순차적으로 찾는 선형 탐색 알고리듬의 원리, 구현 방법, 시간 복잡도를 다룹니다
---

## 선형 탐색이란?

**선형 탐색(Linear Search)**은 배열이나 리스트에서 원하는 값을 찾기 위해 **처음부터 끝까지 순차적으로 확인**하는 가장 기본적인 탐색 알고리듬입니다.

<br>

**문제 상황**

배열 `[5, 3, 8, 1, 9, 2]`에서 값 `8`을 찾고 싶다면:
1. 인덱스 0: `5` - 아님
2. 인덱스 1: `3` - 아님
3. 인덱스 2: `8` - 찾음!

이처럼 배열의 각 원소를 하나씩 확인하며 목표 값을 찾습니다.

<br>

## 선형 탐색의 원리

선형 탐색은 다음과 같은 단계로 동작합니다:

<br>

**1. 첫 번째 원소부터 시작**

배열의 첫 번째 원소와 찾고자 하는 값을 비교합니다.

<br>

**2. 값 비교**

현재 원소가 찾고자 하는 값과 같으면 해당 인덱스를 반환합니다.

<br>

**3. 다음 원소로 이동**

같지 않으면 다음 원소로 이동하여 비교를 반복합니다.

<br>

**4. 끝까지 확인**

배열의 끝까지 확인해도 값을 찾지 못하면 탐색 실패(-1 반환)입니다.

<br>

## 선형 탐색의 구현

선형 탐색은 매우 간단하게 구현할 수 있습니다.

<br>

### 기본 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

int linearSearch(const vector<int>& arr, int target) {
  for (int i = 0; i < arr.size(); i++) {
    if (arr[i] == target) {
      return i;  // 찾으면 인덱스 반환
    }
  }
  return -1;  // 찾지 못하면 -1 반환
}

int main() {
  vector<int> arr = {5, 3, 8, 1, 9, 2};
  int target = 8;

  int result = linearSearch(arr, target);

  if (result != -1) {
    cout << "값 " << target << "은 인덱스 " << result << "에 있습니다.\n";
  } else {
    cout << "값 " << target << "을 찾지 못했습니다.\n";
  }

  return 0;
}
```

**출력**: `값 8은 인덱스 2에 있습니다.`

<br>

### 모든 일치 항목 찾기

값이 여러 번 등장하는 경우, 모든 인덱스를 찾을 수 있습니다.

```cpp
vector<int> linearSearchAll(const vector<int>& arr, int target) {
  vector<int> indices;
  for (int i = 0; i < arr.size(); i++) {
    if (arr[i] == target) {
      indices.push_back(i);
    }
  }
  return indices;
}
```

<br>

### STL 활용

C++ STL의 `find` 함수를 사용하면 더 간결하게 구현할 수 있습니다.

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  vector<int> arr = {5, 3, 8, 1, 9, 2};
  int target = 8;

  auto it = find(arr.begin(), arr.end(), target);

  if (it != arr.end()) {
    cout << "인덱스: " << distance(arr.begin(), it) << "\n";
  } else {
    cout << "찾지 못했습니다.\n";
  }

  return 0;
}
```

<br>

## 시간 복잡도

선형 탐색의 시간 복잡도는 다음과 같습니다:

<br>

| 경우 | 시간 복잡도 | 설명 |
|------|------------|------|
| 최선 | $$O(1)$$ | 첫 번째 원소에서 값을 찾음 |
| 평균 | $$O(n)$$ | 배열 중간쯤에서 값을 찾음 |
| 최악 | $$O(n)$$ | 마지막 원소에서 찾거나 없음 |

<br>

**공간 복잡도**: $$O(1)$$

추가적인 메모리를 사용하지 않습니다.

<br>

## 선형 탐색 vs 이분 탐색

선형 탐색과 [이분 탐색](https://soo-bak.github.io/algorithm/theory/binary-search/)의 차이점을 비교하면:

<br>

| 특성 | 선형 탐색 | 이분 탐색 |
|------|----------|----------|
| 시간 복잡도 | $$O(n)$$ | $$O(\log n)$$ |
| 정렬 필요 | 불필요 | 필요 |
| 구현 난이도 | 매우 쉬움 | 중간 |
| 적합한 상황 | 정렬되지 않은 작은 배열 | 정렬된 큰 배열 |

<br>

**선형 탐색이 적합한 경우**:
- 배열이 정렬되어 있지 않을 때
- 배열의 크기가 작을 때 (약 10~20개 이하)
- 단 한 번만 탐색할 때 (정렬 비용을 고려)

<br>

**이분 탐색이 적합한 경우**:
- 배열이 이미 정렬되어 있을 때
- 배열의 크기가 클 때
- 같은 배열에서 여러 번 탐색할 때

<br>

## 활용 예시

<br>

**1. 특정 값 존재 확인**

정렬되지 않은 데이터에서 특정 값의 존재 여부를 확인할 때 사용합니다.

<br>

**2. 최솟값/최댓값 찾기**

```cpp
int findMax(const vector<int>& arr) {
  int maxVal = arr[0];
  for (int i = 1; i < arr.size(); i++) {
    if (arr[i] > maxVal) {
      maxVal = arr[i];
    }
  }
  return maxVal;
}
```

<br>

**3. 조건을 만족하는 첫 번째 원소 찾기**

```cpp
int findFirst(const vector<int>& arr, function<bool(int)> condition) {
  for (int i = 0; i < arr.size(); i++) {
    if (condition(arr[i])) {
      return i;
    }
  }
  return -1;
}

// 사용 예: 첫 번째 짝수 찾기
int idx = findFirst(arr, [](int x) { return x % 2 == 0; });
```

<br>

## 마무리

선형 탐색은 가장 단순하고 직관적인 탐색 알고리듬입니다.

<br>

**핵심 포인트**
- **순차적 비교**: 처음부터 끝까지 하나씩 비교
- **시간 복잡도**: 평균 및 최악 $$O(n)$$
- **정렬 불필요**: 정렬되지 않은 데이터에서도 사용 가능
- **구현 간단**: 어떤 언어로도 쉽게 구현 가능

<br>

작은 데이터셋이나 정렬되지 않은 데이터에서는 선형 탐색이 효과적입니다.

하지만 데이터가 크고 정렬되어 있다면 [이분 탐색](https://soo-bak.github.io/algorithm/theory/binary-search/)을 사용하는 것이 더 효율적입니다.

<br>

### 관련 글
- [이분 탐색(Binary Search)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/binary-search/)


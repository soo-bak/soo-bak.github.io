---
layout: single
title: "선형 탐색(Linear Search)의 원리와 구현 - soo:bak"
date: "2026-01-03 01:00:00 +0900"
description: 배열에서 원하는 값을 순차적으로 찾는 선형 탐색 알고리듬의 원리, 구현 방법, 시간 복잡도를 다룹니다
---

## 선형 탐색이란?

배열 `[5, 3, 8, 1, 9, 2]`에서 값 `8`을 찾아야 한다고 가정해보겠습니다.

가장 직관적인 방법은 배열의 첫 번째 원소부터 하나씩 확인하는 것입니다.

- 인덱스 0: `5` → 아님
- 인덱스 1: `3` → 아님
- 인덱스 2: `8` → 찾음!

<br>

이처럼 배열의 처음부터 끝까지 순차적으로 확인하며 원하는 값을 찾는 방법을 **선형 탐색(Linear Search)**이라고 합니다.

구현이 매우 간단하고, 배열이 정렬되어 있지 않아도 사용할 수 있다는 장점이 있습니다.

---

## 선형 탐색의 동작 원리

선형 탐색은 다음과 같은 단계로 동작합니다:

1. 배열의 첫 번째 원소부터 시작
2. 현재 원소가 찾고자 하는 값과 같으면 해당 인덱스를 반환
3. 같지 않으면 다음 원소로 이동하여 비교를 반복
4. 배열의 끝까지 확인해도 값을 찾지 못하면 탐색 실패

<br>

단순하지만, 배열의 모든 원소를 확인해야 할 수도 있기 때문에 배열의 크기가 커지면 비효율적일 수 있습니다.

---

## 구현

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

값이 여러 번 등장하는 경우, 모든 인덱스를 찾아야 할 때도 있습니다.

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

---

## 시간 복잡도

선형 탐색의 시간 복잡도는 다음과 같습니다:

- **최선의 경우**: $$O(1)$$ - 첫 번째 원소에서 바로 찾는 경우
- **평균적인 경우**: $$O(n)$$ - 배열 중간쯤에서 찾는 경우
- **최악의 경우**: $$O(n)$$ - 마지막 원소에서 찾거나 배열에 없는 경우

<br>

공간 복잡도는 $$O(1)$$로, 추가적인 메모리를 사용하지 않습니다.

---

## 선형 탐색의 활용

### 최솟값/최댓값 찾기

배열에서 최댓값을 찾는 것도 선형 탐색의 일종입니다.

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

### 조건을 만족하는 첫 번째 원소 찾기

특정 조건을 만족하는 첫 번째 원소의 인덱스를 찾을 수도 있습니다.

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

---

## 선형 탐색 vs 이분 탐색

선형 탐색은 정렬되지 않은 데이터에서도 사용할 수 있다는 장점이 있지만, 데이터가 많아지면 비효율적입니다.

반면, 이분 탐색은 정렬된 데이터에서만 사용할 수 있지만 $$O(\log n)$$의 시간 복잡도로 훨씬 빠릅니다.

<br>

**선형 탐색이 적합한 경우**:
- 배열이 정렬되어 있지 않을 때
- 배열의 크기가 작을 때 (약 10~20개 이하)
- 단 한 번만 탐색할 때 (정렬 비용을 고려하면 선형 탐색이 유리)

<br>

**이분 탐색이 적합한 경우**:
- 배열이 이미 정렬되어 있을 때
- 배열의 크기가 클 때
- 같은 배열에서 여러 번 탐색할 때

<br>

> 참고: [이분 탐색(Binary Search)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/binary-search/)

---

## 마무리

선형 탐색은 가장 단순하고 직관적인 탐색 알고리듬입니다.

구현이 쉽고 정렬되지 않은 데이터에서도 사용할 수 있지만, 배열의 크기가 커지면 비효율적입니다.

<br>

작은 데이터셋이나 정렬되지 않은 데이터에서는 선형 탐색이 효과적이지만,

데이터가 크고 정렬되어 있다면 이분 탐색을 사용하는 것이 더 효율적입니다.

<br>

**관련 글**:
- [이분 탐색(Binary Search)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/binary-search/)

<br>

**관련 문제**:
- [[백준 2750] 수 정렬하기](https://soo-bak.github.io/algorithm/boj/SortingNumbers-65/)
- [[백준 2562] 최댓값](https://soo-bak.github.io/algorithm/boj/maxNum-55/)


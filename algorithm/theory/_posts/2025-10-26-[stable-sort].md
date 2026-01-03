---
layout: single
title: "안정 정렬(Stable Sort)의 개념과 특성 - soo:bak"
date: "2025-10-26 05:00:00 +0900"
description: 같은 값을 가진 원소들의 상대적 순서를 유지하는 안정 정렬의 정의, 특성, 구현 방법, 그리고 다양한 정렬 알고리듬의 안정성을 다룹니다
tags:
  - 정렬
---

## 안정 정렬이란?

**안정 정렬(Stable Sort)**은 정렬 과정에서 같은 값을 가진 원소들의 **상대적 순서를 유지**하는 정렬 방식입니다.

반면 **불안정 정렬(Unstable Sort)**은 같은 값을 가진 원소들의 순서가 바뀔 수 있습니다.

<br>

다음 예시로 두 방식의 차이를 살펴보겠습니다:

```
초기 배열: [(A, 85), (B, 90), (C, 85), (D, 90)]
```

두 번째 요소(점수)를 기준으로 정렬할 때:

**안정 정렬**:
```
결과: [(A, 85), (C, 85), (B, 90), (D, 90)]
```
점수 85인 A와 C의 순서가 유지되고, 점수 90인 B와 D의 순서도 유지됩니다.

**불안정 정렬**:
```
결과: [(C, 85), (A, 85), (D, 90), (B, 90)]  (가능한 결과 중 하나)
```
같은 값을 가진 원소들의 순서가 바뀔 수 있습니다.

---

## 안정성의 필요성

안정 정렬은 다중 키 정렬과 데이터 구조 유지가 필요한 상황에서 중요합니다.

<br>

### 다단계 정렬

여러 기준으로 정렬할 때 안정 정렬을 활용하면 각 단계의 정렬 결과가 누적됩니다.

{% raw %}
```
초기 데이터: [(1학년, 85점), (2학년, 90점), (1학년, 90점), (2학년, 85점)]

1단계: 점수순 정렬 (안정)
→ [(1학년, 85점), (2학년, 85점), (2학년, 90점), (1학년, 90점)]

2단계: 학년순 정렬 (안정)
→ [(1학년, 85점), (1학년, 90점), (2학년, 85점), (2학년, 90점)]
```
{% endraw %}

같은 학년 내에서 점수 순서가 자동으로 유지됩니다.

<br>

### 원본 순서 보존

```cpp
struct Product {
  int id;
  int price;
};

vector<Product> products = {
  {1, 1000},
  {2, 2000},
  {3, 1000}
};

// 가격순 정렬 (안정)
stable_sort(products.begin(), products.end(),
  [](const Product& a, const Product& b) {
    return a.price < b.price;
  });

// 결과: [{1, 1000}, {3, 1000}, {2, 2000}]
// 같은 가격 내에서 id 순서 유지
```

2차 정렬 키를 명시하지 않아도 원본 순서가 보존됩니다.

---

## 정렬 알고리듬의 안정성

주요 정렬 알고리듬을 안정성 기준으로 분류하면 다음과 같습니다.

<br>

### 안정 정렬 알고리듬

| 알고리듬 | 평균 시간 복잡도 | 공간 복잡도 | 특징 |
|---------|---------------|-----------|------|
| 병합 정렬 | $$O(n \log n)$$ | $$O(n)$$ | 병합 시 좌측 우선 선택 |
| 삽입 정렬 | $$O(n^2)$$ | $$O(1)$$ | 같은 값은 이동하지 않음 |
| 버블 정렬 | $$O(n^2)$$ | $$O(1)$$ | 인접 원소만 교환 |
| Tim Sort | $$O(n \log n)$$ | $$O(n)$$ | 병합 정렬 기반 |

<br>

### 불안정 정렬 알고리듬

| 알고리듬 | 평균 시간 복잡도 | 공간 복잡도 | 특징 |
|---------|---------------|-----------|------|
| 빠른 정렬 | $$O(n \log n)$$ | $$O(\log n)$$ | 피벗 기준 교환 |
| 힙 정렬 | $$O(n \log n)$$ | $$O(1)$$ | 힙 구조 재구성 |
| 선택 정렬 | $$O(n^2)$$ | $$O(1)$$ | 최솟값과 교환 |

<br>

> 참고: [병합 정렬(Merge Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/merge-sort/)

> 참고: [삽입 정렬(Insertion Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/insertion-sort/)

> 참고: [빠른 정렬(Quick Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/quick-sort/)

> 참고: [힙 정렬(Heap Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/heap-sort/)

---

## 안정성 구현 원리

각 정렬 알고리듬의 안정성 여부는 비교와 교환 방식에 따라 결정됩니다.

<br>

### 병합 정렬의 안정성

병합 과정에서 같은 값일 때 왼쪽 부분 배열의 원소를 먼저 선택하면 안정성이 보장됩니다.

```cpp
void merge(vector<int>& arr, int left, int mid, int right) {
  vector<int> temp(right - left + 1);
  int i = left, j = mid + 1, k = 0;
  
  while (i <= mid && j <= right) {
    // 같을 때 왼쪽을 먼저 선택
    if (arr[i] <= arr[j]) {
      temp[k++] = arr[i++];
    } else {
      temp[k++] = arr[j++];
    }
  }
  
  while (i <= mid) temp[k++] = arr[i++];
  while (j <= right) temp[k++] = arr[j++];
  
  for (int idx = 0; idx < temp.size(); idx++) {
    arr[left + idx] = temp[idx];
  }
}
```

`arr[i] <= arr[j]` 조건의 `<=` 연산자가 핵심입니다.

`<`를 사용하면 같은 값일 때 오른쪽이 먼저 선택되어 불안정해집니다.

<br>

### 삽입 정렬의 안정성

삽입 과정에서 같은 값을 만나면 이동을 중단합니다.

```cpp
void insertionSort(vector<int>& arr) {
  for (int i = 1; i < arr.size(); i++) {
    int key = arr[i];
    int j = i - 1;
    
    // key보다 큰 값만 이동
    while (j >= 0 && arr[j] > key) {
      arr[j + 1] = arr[j];
      j--;
    }
    
    arr[j + 1] = key;
  }
}
```

`arr[j] > key` 조건에서 같은 값일 때는 이동하지 않아 원래 순서가 유지됩니다.

<br>

### 빠른 정렬의 불안정성

피벗을 기준으로 원소를 교환하는 과정에서 같은 값을 가진 원소들의 순서가 바뀔 수 있습니다.

```cpp
int partition(vector<int>& arr, int low, int high) {
  int pivot = arr[high];
  int i = low - 1;
  
  for (int j = low; j < high; j++) {
    if (arr[j] < pivot) {
      i++;
      swap(arr[i], arr[j]);  // 교환 발생
    }
  }
  
  swap(arr[i + 1], arr[high]);
  return i + 1;
}
```

{% raw %}
예시: `[3₁, 5, 3₂, 1]`을 피벗 `1`로 분할할 때

- `j = 0`: `3₁ < 1` 거짓
- `j = 1`: `5 < 1` 거짓
- `j = 2`: `3₂ < 1` 거짓
- 분할 후: `[1, 5, 3₂, 3₁]` → `3₁`과 `3₂`의 순서가 바뀜
{% endraw %}

---

## 불안정 정렬의 안정화

불안정 정렬을 안정 정렬로 변환하는 방법들이 있습니다.

<br>

### 방법 1: 인덱스 기반 비교

원본 인덱스를 추가하여 같은 값일 때 인덱스로 비교합니다.

```cpp
struct Element {
  int value;
  int index;
};

int n = original.size();
vector<Element> arr(n);
for (int i = 0; i < n; i++) {
  arr[i] = {original[i], i};
}

// 값이 같으면 인덱스로 비교
sort(arr.begin(), arr.end(), 
  [](const Element& a, const Element& b) {
    if (a.value != b.value) return a.value < b.value;
    return a.index < b.index;
  });
```

**시간 복잡도**: $$O(n \log n)$$

**공간 복잡도**: $$O(n)$$

<br>

### 방법 2: stable_sort 사용

C++ STL의 `stable_sort`는 안정 정렬을 보장합니다.

{% raw %}
```cpp
vector<pair<int, int>> arr = {{3, 1}, {1, 2}, {3, 3}, {1, 4}};

stable_sort(arr.begin(), arr.end(), 
  [](const pair<int, int>& a, const pair<int, int>& b) {
    return a.first < b.first;
  });

// 결과: (1, 2) (1, 4) (3, 1) (3, 3)
```
{% endraw %}

`stable_sort`는 내부적으로 병합 정렬을 기반으로 구현됩니다.

---

## C++ STL 정렬 함수 비교

<br>

### std::sort

```cpp
vector<int> arr = {3, 1, 3, 2, 1};
sort(arr.begin(), arr.end());
```

| 특성 | 설명 |
|------|------|
| 안정성 | 불안정 |
| 알고리듬 | 인트로 정렬 (빠른 정렬 + 힙 정렬 + 삽입 정렬) |
| 시간 복잡도 | 평균/최악 $$O(n \log n)$$ |
| 공간 복잡도 | $$O(\log n)$$ |

<br>

### std::stable_sort

```cpp
vector<int> arr = {3, 1, 3, 2, 1};
stable_sort(arr.begin(), arr.end());
```

| 특성 | 설명 |
|------|------|
| 안정성 | 안정 |
| 알고리듬 | 병합 정렬 기반 |
| 시간 복잡도 | $$O(n \log n)$$ |
| 공간 복잡도 | $$O(n)$$ |

<br>

### 성능 비교

```
데이터: 100,000개
sort:        약 10ms
stable_sort: 약 15ms
```

안정성이 불필요한 경우 `sort`를, 안정성이 필요한 경우 `stable_sort`를 사용합니다.

---

## 활용 예시

<br>

### 다중 키 정렬

{% raw %}
```cpp
struct Data {
  int primary;
  int secondary;
  int id;
};

vector<Data> arr = {
  {1, 85, 0},
  {2, 90, 1},
  {1, 90, 2},
  {2, 85, 3}
};

// 1단계: secondary 기준 정렬
stable_sort(arr.begin(), arr.end(),
  [](const Data& a, const Data& b) {
    return a.secondary > b.secondary;
  });

// 2단계: primary 기준 정렬
stable_sort(arr.begin(), arr.end(),
  [](const Data& a, const Data& b) {
    return a.primary < b.primary;
  });

// 결과: primary가 같으면 secondary 순서 유지
```
{% endraw %}

<br>

### 타임스탬프 기반 정렬

```cpp
struct Event {
  long long timestamp;
  int type;
  int id;
};

vector<Event> events;

// 타임스탬프로 정렬, 같은 시간이면 입력 순서 유지
stable_sort(events.begin(), events.end(),
  [](const Event& a, const Event& b) {
    return a.timestamp < b.timestamp;
  });
```

<br>

### 부분 정렬 보존

```cpp
// 이미 정렬된 데이터에 추가 정렬 적용
vector<Item> items = {...};  // category로 정렬됨

// price로 재정렬, 같은 price면 category 순서 유지
stable_sort(items.begin(), items.end(),
  [](const Item& a, const Item& b) {
    return a.price < b.price;
  });
```

---

## 안정성 검증

<br>

### 테스트 구현

{% raw %}
```cpp
#include <bits/stdc++.h>
using namespace std;

bool isStable(vector<pair<int, int>>& arr) {
  stable_sort(arr.begin(), arr.end(),
    [](const pair<int, int>& a, const pair<int, int>& b) {
      return a.first < b.first;
    });
  
  // 같은 first 값끼리 second 값의 순서 확인
  for (int i = 1; i < arr.size(); i++) {
    if (arr[i].first == arr[i-1].first) {
      if (arr[i].second < arr[i-1].second) {
        return false;
      }
    }
  }
  
  return true;
}

int main() {
  vector<pair<int, int>> arr = {
    {3, 0}, {1, 1}, {3, 2}, {1, 3}, {2, 4}
  };
  
  cout << (isStable(arr) ? "stable" : "unstable") << "\n";
  
  return 0;
}
```
{% endraw %}

---

## 마무리

안정 정렬은 같은 값을 가진 원소들의 상대적 순서를 유지하는 정렬 방식입니다.

<br>

병합 정렬, 삽입 정렬은 안정 정렬이며, 빠른 정렬, 힙 정렬은 불안정 정렬입니다.

C++ STL에서는 `stable_sort`를 통해 안정 정렬을 사용할 수 있습니다.

<br>

다중 키 정렬이나 원본 순서 보존이 필요한 경우 안정 정렬이 필수적이며,

불안정 정렬을 안정하게 만들기 위해서는 인덱스를 추가하거나 `stable_sort`를 사용할 수 있습니다.

<br>

**관련 글**:
- [병합 정렬(Merge Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/merge-sort/)
- [삽입 정렬(Insertion Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/insertion-sort/)
- [빠른 정렬(Quick Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/quick-sort/)
- [힙 정렬(Heap Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/heap-sort/)

<br>

**관련 문제**:
- [[백준 2750] 수 정렬하기](https://soo-bak.github.io/algorithm/boj/SortingNumbers-65/)
- [[백준 2751] 수 정렬하기 2](https://soo-bak.github.io/algorithm/boj/SortingNumbers-2-75/)
- [[백준 11931] 수 정렬하기 4](https://soo-bak.github.io/algorithm/boj/sortdesc-44/)

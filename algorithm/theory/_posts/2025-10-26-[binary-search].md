---
layout: single
title: "이분 탐색(Binary Search)의 원리와 구현 - soo:bak"
date: "2025-10-26 00:00:00 +0900"
description: 정렬된 배열에서 특정 값을 효율적으로 찾는 이분 탐색의 원리, 구현 방법, 시간 복잡도, 그리고 다양한 활용 방법을 다룹니다
tags:
  - 이분탐색
---

## 이분 탐색이란?

**이분 탐색(Binary Search)**은 정렬된 배열에서 특정 값을 찾을 때, 탐색 범위를 절반씩 줄여나가며 효율적으로 값을 찾는 알고리듬입니다.

매 단계마다 검색 범위를 절반으로 줄이기 때문에 $$O(\log n)$$의 시간 복잡도를 가지며, 선형 탐색의 $$O(n)$$에 비해 매우 빠른 탐색이 가능합니다.

---

## 이분 탐색의 원리

이분 탐색은 다음과 같은 과정으로 동작합니다:

1. **범위 설정**: 탐색 범위의 시작(`left`)과 끝(`right`)을 설정
2. **중간 값 확인**: 중간 위치(`mid`)의 값을 확인
3. **범위 조정**:
   - 중간 값이 찾는 값과 같으면 탐색 종료
   - 중간 값이 찾는 값보다 크면 왼쪽 절반 탐색 (`right = mid - 1`)
   - 중간 값이 찾는 값보다 작으면 오른쪽 절반 탐색 (`left = mid + 1`)
4. **반복**: 범위가 유효한 동안 2~3번 반복

<br>

### 단계별 예시

정렬된 배열 `[1, 3, 5, 7, 9, 11, 13, 15, 17, 19]`에서 값 `7`을 찾는 과정:

**1단계**: `left = 0`, `right = 9`, `mid = 4`
- `arr[4] = 9 > 7` → 오른쪽 절반 제거
- `right = 3`으로 갱신

**2단계**: `left = 0`, `right = 3`, `mid = 1`
- `arr[1] = 3 < 7` → 왼쪽 절반 제거
- `left = 2`로 갱신

**3단계**: `left = 2`, `right = 3`, `mid = 2`
- `arr[2] = 5 < 7` → 왼쪽 절반 제거
- `left = 3`으로 갱신

**4단계**: `left = 3`, `right = 3`, `mid = 3`
- `arr[3] = 7 == 7` → 찾음!

---

## 구현

### 반복 구현

가장 일반적이고 효율적인 구현 방식입니다.

```cpp
#include <bits/stdc++.h>
using namespace std;

// 배열 arr에서 target을 찾아 인덱스 반환, 없으면 -1 반환
int binarySearch(vector<int>& arr, int target) {
  int left = 0;
  int right = arr.size() - 1;
  
  while (left <= right) {
    int mid = left + (right - left) / 2;  // 오버플로우 방지
    
    if (arr[mid] == target) {
      return mid;  // 찾음
    }
    else if (arr[mid] < target) {
      left = mid + 1;  // 오른쪽 절반 탐색
    }
    else {
      right = mid - 1;  // 왼쪽 절반 탐색
    }
  }
  
  return -1;  // 못 찾음
}

int main() {
  vector<int> arr = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
  int target = 7;
  
  int result = binarySearch(arr, target);
  if (result != -1) {
    cout << "Found at index " << result << "\n";
  } else {
    cout << "Not found\n";
  }
  
  return 0;
}
```

**중요 포인트**:
- `mid = left + (right - left) / 2`를 사용하여 오버플로우 방지
- `left <= right` 조건으로 범위가 교차할 때까지 탐색
- 매 단계마다 `left` 또는 `right`를 갱신하여 범위 축소

<br>

**장점**:
- 반복문 사용으로 스택 오버플로우 걱정 없음
- 실행 속도가 미세하게 더 빠름
- 실전에서 가장 많이 사용됨

<br>

### 재귀 구현

수학적 정의에 가까운 형태입니다.

```cpp
#include <bits/stdc++.h>
using namespace std;

int binarySearchRecursive(vector<int>& arr, int target, int left, int right) {
  // 기저 조건: 범위가 유효하지 않으면 -1 반환
  if (left > right) return -1;
  
  int mid = left + (right - left) / 2;
  
  if (arr[mid] == target) {
    return mid;  // 찾음
  }
  else if (arr[mid] < target) {
    return binarySearchRecursive(arr, target, mid + 1, right);  // 오른쪽
  }
  else {
    return binarySearchRecursive(arr, target, left, mid - 1);  // 왼쪽
  }
}

int main() {
  vector<int> arr = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
  int target = 7;
  
  int result = binarySearchRecursive(arr, target, 0, arr.size() - 1);
  if (result != -1) {
    cout << "Found at index " << result << "\n";
  } else {
    cout << "Not found\n";
  }
  
  return 0;
}
```

**장점**:
- 코드가 간결하고 직관적
- 분할 정복의 개념을 명확히 보여줌

**단점**:
- 재귀 호출 오버헤드 발생
- 매우 큰 배열에서는 스택 오버플로우 가능성 (실제로는 거의 발생하지 않음)

<br>

C++ 표준 라이브러리에서는 `<algorithm>` 헤더의 `binary_search(begin, end, value)` 함수를 제공합니다.

이 함수는 값의 존재 여부를 `bool`로 반환합니다.

<br>

이분 탐색을 사용하기 전에는 반드시 배열이 정렬되어 있어야 합니다.

정렬되지 않은 배열이라면 먼저 정렬을 수행해야 하는데, 이 때 [빠른 정렬(Quick Sort)](https://soo-bak.github.io/algorithm/theory/quick-sort/)이나 [삽입 정렬(Insertion Sort)](https://soo-bak.github.io/algorithm/theory/insertion-sort/) 등의 정렬 알고리듬을 활용할 수 있습니다.

---

## 시간 복잡도

### 시간 복잡도

이분 탐색의 시간 복잡도는 다음과 같습니다:

$$
O(\log n)
$$

매 단계마다 탐색 범위가 절반으로 줄어들기 때문에, 크기 $$n$$인 배열에서 최대 $$\log_2 n$$번의 비교만 수행합니다.

<br>

**비교 예시**:

| 배열 크기 | 순차 탐색 (최악) | 이분 탐색 (최악) |
|----------|---------------|---------------|
| 10 | 10번 | 4번 |
| 100 | 100번 | 7번 |
| 1,000 | 1,000번 | 10번 |
| 1,000,000 | 1,000,000번 | 20번 |
| 1,000,000,000 | 1,000,000,000번 | 30번 |

배열의 크기가 커질수록 이분 탐색의 효율성이 뚜렷히 드러납니다.

<br>

### 공간 복잡도

- 반복 구현: $$O(1)$$ (추가 공간 거의 불필요)
- 재귀 구현: $$O(\log n)$$ (재귀 스택)

---

## 이분 탐색의 활용

### 1) Lower Bound (하한)

정렬된 배열에서 `target` 이상인 값이 처음 나타나는 위치를 찾습니다.

```cpp
int lowerBound(vector<int>& arr, int target) {
  int left = 0;
  int right = arr.size();  // arr.size() - 1이 아님!
  
  while (left < right) {
    int mid = left + (right - left) / 2;
    
    if (arr[mid] < target) {
      left = mid + 1;
    }
    else {
      right = mid;  // mid도 가능한 답일 수 있음
    }
  }
  
  return left;
}
```

**활용**: 특정 값 이상의 원소들의 개수를 세거나, 삽입 위치를 찾을 때 사용

<br>

### 2) Upper Bound (상한)

정렬된 배열에서 `target`을 초과하는 값이 처음 나타나는 위치를 찾습니다.

```cpp
int upperBound(vector<int>& arr, int target) {
  int left = 0;
  int right = arr.size();
  
  while (left < right) {
    int mid = left + (right - left) / 2;
    
    if (arr[mid] <= target) {  // <= 주의
      left = mid + 1;
    }
    else {
      right = mid;
    }
  }
  
  return left;
}
```

**활용**: 특정 값의 개수를 셀 때 `upperBound(target) - lowerBound(target)`으로 계산

C++ 표준 라이브러리에서는 `std::lower_bound`와 `std::upper_bound`를 제공합니다.

Lower Bound와 Upper Bound는 정렬된 배열에서 특정 조건을 만족하는 구간을 찾을 때 유용하며, [투 포인터(Two Pointer)](https://soo-bak.github.io/algorithm/theory/two-pointer-explained/)나 [슬라이딩 윈도우(Sliding Window)](https://soo-bak.github.io/algorithm/theory/sliding-window-explained/) 기법과 함께 활용되기도 합니다.

<br>

### 3) 파라메트릭 서치 (Parametric Search)

이분 탐색의 응용으로, **결정 문제**를 최적화 문제로 변환하여 해결합니다.

"최소 $$x$$를 구하라" 문제를 "$$x$$ 이상이 가능한가?"의 반복으로 풀이합니다.

<br>

**대표 예시: 랜선 자르기**
- `N`개의 랜선을 자르되, 적어도 `K`개를 만들 수 있는 최대 길이는?
- 길이를 이분 탐색하며, 각 길이로 `K`개 이상 만들 수 있는지 확인

```cpp
bool canCut(vector<int>& cables, int length, int k) {
  int count = 0;
  for (int cable : cables) {
    count += cable / length;
  }
  return count >= k;
}

int findMaxLength(vector<int>& cables, int k) {
  int left = 1;
  int right = *max_element(cables.begin(), cables.end());
  int answer = 0;
  
  while (left <= right) {
    int mid = left + (right - left) / 2;
    
    if (canCut(cables, mid, k)) {
      answer = mid;  // 가능하면 답 갱신
      left = mid + 1;  // 더 큰 값 탐색
    }
    else {
      right = mid - 1;  // 더 작은 값 탐색
    }
  }
  
  return answer;
}
```

파라메트릭 서치는 최적화 문제를 결정 문제로 변환하여 풀이하는 방식으로, [그리디 알고리듬(Greedy Algorithm)](https://soo-bak.github.io/algorithm/theory/greedyAlgo/)이나 [동적 계획법(Dynamic Programming)](https://soo-bak.github.io/algorithm/theory/dynamic-programming/)과 함께 활용되기도 합니다.

<br>

### 4) 실수 이분 탐색

정수가 아닌 실수 범위에서도 이분 탐색을 적용할 수 있습니다.

```cpp
double findSquareRoot(double n) {
  double left = 0.0;
  double right = n;
  double epsilon = 1e-9;  // 정밀도
  
  while (right - left > epsilon) {
    double mid = (left + right) / 2.0;
    
    if (mid * mid < n) {
      left = mid;
    }
    else {
      right = mid;
    }
  }
  
  return left;
}
```

**주의**: 정수처럼 `left <= right` 조건을 사용하면 무한 루프에 빠질 수 있으므로, 정밀도 기반 종료 조건 사용

---

## 실전 예제: 수 찾기

### 문제

$$N$$개의 정수가 주어지고, $$M$$개의 수가 주어졌을 때, 각 수가 배열에 존재하는지 판별하는 프로그램을 작성하시오.

- 제약: $$1 \leq N, M \leq 100,000$$
- 입력: 
  - 첫째 줄에 $$N$$
  - 둘째 줄에 $$N$$개의 정수
  - 셋째 줄에 $$M$$
  - 넷째 줄에 $$M$$개의 정수
- 출력: 각 수가 존재하면 `1`, 아니면 `0` 출력 (한 줄에 하나씩)

<br>

### 접근법

1. $$N$$개의 정수를 배열에 저장하고 정렬
2. $$M$$개의 각 수에 대해 이분 탐색으로 존재 여부 확인
3. 존재하면 `1`, 아니면 `0` 출력

<br>

### 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

int binarySearch(vector<int>& arr, int target) {
  int left = 0;
  int right = arr.size() - 1;
  
  while (left <= right) {
    int mid = left + (right - left) / 2;
    
    if (arr[mid] == target) {
      return 1;  // 존재
    }
    else if (arr[mid] < target) {
      left = mid + 1;
    }
    else {
      right = mid - 1;
    }
  }
  
  return 0;  // 존재하지 않음
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);
  
  int n;
  cin >> n;
  
  vector<int> arr(n);
  for (int i = 0; i < n; i++) {
    cin >> arr[i];
  }
  
  // 정렬 (이분 탐색의 전제 조건)
  sort(arr.begin(), arr.end());
  
  int m;
  cin >> m;
  
  while (m--) {
    int target;
    cin >> target;
    cout << binarySearch(arr, target) << "\n";
  }
  
  return 0;
}
```

<br>

### 시간 복잡도

- 정렬: $$O(N \log N)$$
- 각 쿼리에 대한 이분 탐색: $$O(\log N)$$
- 전체 쿼리: $$O(M \log N)$$
- **전체**: $$O(N \log N + M \log N)$$

만약 이분 탐색 없이 순차 탐색을 사용했다면 $$O(N \times M) = O(10^{10})$$로 굉장히 오랜 연산 시간을 필요로 합니다.

---

## 마무리

이분 탐색은 정렬된 데이터에서 특정 값을 찾을 때 사용하는 가장 효율적인 알고리듬 중 하나입니다.

$$O(\log n)$$의 시간 복잡도는 대용량 데이터 처리에서 효율적인 성능을 발휘합니다.

<br>

이분 탐색의 핵심은 **탐색 범위를 절반씩 줄여나가는 것**이며, 이를 위해서는 데이터가 **정렬되어 있어야 한다**는 전제 조건이 필요합니다.

단순한 값 탐색뿐만 아니라, Lower Bound/Upper Bound를 통한 구간 탐색, 파라메트릭 서치를 통한 최적화 문제 해결 등 다양하게 활용할 수 있습니다.

<br>

알고리듬 문제에서 탐색 문제를 만났을 때, 데이터가 정렬되어 있거나 정렬 가능하다면 이분 탐색을 떠올리시면 도움이 됩니다.

<br>

**이분 탐색 사용 판단 기준**:
- 데이터가 정렬되어 있거나 정렬 가능한가?
- 탐색 공간의 크기가 큰가? ($$10^5$$ 이상)
- 결정 문제로 변환 가능한 최적화 문제인가?

<br>

**관련 글**:
- [빠른 정렬(Quick Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/quick-sort/)
- [삽입 정렬(Insertion Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/insertion-sort/)
- [투 포인터(Two Pointer)의 원리와 활용 - soo:bak](https://soo-bak.github.io/algorithm/theory/two-pointer-explained/)
- [슬라이딩 윈도우(Sliding Window)의 원리와 활용 - soo:bak](https://soo-bak.github.io/algorithm/theory/sliding-window-explained/)
- [그리디 알고리듬(Greedy Algorithm, 탐욕법)의 원리와 적용 - soo:bak](https://soo-bak.github.io/algorithm/theory/greedyAlgo/)
- [동적 계획법(Dynamic Programming)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/dynamic-programming/)

<br>

**관련 문제**:
- [[백준 1920] 수 찾기](https://soo-bak.github.io/algorithm/boj/FindingNum-39/)
- [[백준 1654] 랜선 자르기](https://soo-bak.github.io/algorithm/boj/CuttingLines-37/)
- [[백준 2805] 나무 자르기](https://soo-bak.github.io/algorithm/boj/CuttingTrees-44/)
- [[백준 10816] 숫자 카드 2](https://soo-bak.github.io/algorithm/boj/numberCardTwo-43/)
- [[백준 1822] 차집합](https://soo-bak.github.io/algorithm/boj/set-diff-21/)


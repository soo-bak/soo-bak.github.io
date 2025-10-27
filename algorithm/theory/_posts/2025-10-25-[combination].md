---
layout: single
title: "조합(Combination)의 원리와 구현 - soo:bak"
date: "2025-10-25 00:00:00 +0900"
description: 조합의 수학적 정의, 재귀와 백트래킹을 활용한 조합 생성 방법, 시간 복잡도, 다양한 응용을 상세히 설명한 글
---

## 조합이란?

**조합(Combination)**은 $$n$$개의 원소 중에서 순서와 관계없이 $$r$$개를 선택하는 경우의 수를 의미합니다.

순열과 달리 선택된 원소들의 순서를 고려하지 않습니다. 

예를 들어, 집합 $$\{1, 2, 3\}$$에서 2개를 선택하는 경우 순열에서는 $$(1, 2)$$와 $$(2, 1)$$을 서로 다른 경우로 세지만, 조합에서는 이 둘을 같은 경우로 봅니다.

<br>
따라서 $$\{1, 2, 3\}$$에서 2개를 선택하는 조합은 다음 3가지입니다:

$$
\{1, 2\}, \{1, 3\}, \{2, 3\}
$$

<br>
조합은 집합에서 특정 개수의 원소를 뽑는 문제에서 자주 등장하며, 알고리즘 문제뿐만 아니라 확률, 통계, 조합론 등 다양한 수학 분야의 기초가 됩니다.

<br>

---

## 조합의 수학적 정의

$$n$$개 중 $$r$$개를 선택하는 조합의 개수는 다음과 같이 표현됩니다:

$$
C(n, r) = \binom{n}{r} = \frac{n!}{r!(n-r)!}
$$

<br>
이 식이 성립하는 이유는 다음과 같습니다.

먼저 $$n$$개 중 $$r$$개를 순서를 고려하여 선택하는 순열의 개수는 $$P(n, r) = \frac{n!}{(n-r)!}$$입니다.

그런데 조합에서는 순서를 고려하지 않으므로, 같은 원소로 이루어진 $$r!$$가지의 순열은 모두 하나의 조합으로 세어야 합니다.

따라서 순열의 개수를 $$r!$$로 나누면 조합의 개수가 됩니다.

<br>

### 조합의 기본 성질

조합은 다음과 같은 중요한 성질들을 가집니다:

<br>

**1. 공집합과 전체 집합**

$$
\binom{n}{0} = \binom{n}{n} = 1
$$

$$n$$개 중 하나도 선택하지 않는 경우와 모두 선택하는 경우는 각각 1가지입니다.

<br>

**2. 대칭성**

$$
\binom{n}{r} = \binom{n}{n-r}
$$

$$n$$개 중 $$r$$개를 선택하는 것은 $$(n-r)$$개를 선택하지 않는 것과 같습니다.

예를 들어, 5개 중 2개를 선택하는 경우의 수는 5개 중 3개를 선택하는 경우의 수와 같습니다.

<br>

**3. 파스칼의 삼각형**

$$
\binom{n}{r} = \binom{n-1}{r-1} + \binom{n-1}{r}
$$

이는 특정 원소를 포함하는 경우와 포함하지 않는 경우로 나누어 생각할 수 있기 때문입니다.

예를 들어, $$n$$개 중 $$r$$개를 선택할 때 특정 원소 $$x$$를 기준으로 나누면:

- $$x$$를 포함하는 경우: 나머지 $$(n-1)$$개 중 $$(r-1)$$개를 선택 → $$\binom{n-1}{r-1}$$
- $$x$$를 포함하지 않는 경우: 나머지 $$(n-1)$$개 중 $$r$$개를 선택 → $$\binom{n-1}{r}$$

<br>
이 성질은 동적 계획법으로 조합의 개수를 효율적으로 계산하는 데 활용됩니다.

<br>

---

## 조합의 개수 계산

### 1. 팩토리얼을 이용한 계산

```cpp
#include <bits/stdc++.h>
using namespace std;

long long factorial(int n) {
  long long result = 1;
  for (int i = 2; i <= n; i++) {
    result *= i;
  }
  return result;
}

long long combination(int n, int r) {
  if (r > n) return 0;
  if (r == 0 || r == n) return 1;
  return factorial(n) / (factorial(r) * factorial(n - r));
}
```

<br>
이 방법은 $$n$$이 작을 때는 유용하지만, $$n$$이 커지면 오버플로우가 발생할 수 있습니다.

<br>

### 2. 동적 계획법을 이용한 계산

파스칼의 삼각형 성질 $$\binom{n}{r} = \binom{n-1}{r-1} + \binom{n-1}{r}$$을 활용하면 조합의 개수를 효율적으로 계산할 수 있습니다.

<br>

#### 파스칼의 삼각형이란?

**파스칼의 삼각형(Pascal's Triangle)** 은 이항 계수들을 삼각형 형태로 배열한 것입니다.

각 행은 $$(a + b)^n$$을 전개했을 때의 계수를 나타내며, 각 수는 바로 위의 두 수의 합으로 구성됩니다:

```
              1                  ← C(0,0)
            1   1                ← C(1,0) C(1,1)
          1   2   1              ← C(2,0) C(2,1) C(2,2)
        1   3   3   1            ← C(3,0) C(3,1) C(3,2) C(3,3)
      1   4   6   4   1          ← C(4,0) C(4,1) C(4,2) C(4,3) C(4,4)
    1   5  10  10   5   1        ← C(5,0) C(5,1) C(5,2) C(5,3) C(5,4) C(5,5)
```

<br>
예를 들어, $$\binom{4}{2} = 6$$은 4번째 행의 2번째 위치에 있으며,

이는 위의 두 수 $$\binom{3}{1} = 3$$과 $$\binom{3}{2} = 3$$의 합으로 구성됩니다.

<br>

**흥미로운 성질**: 파스칼의 삼각형의 대각선에는 다양한 수열이 숨어 있습니다.

- 첫 번째 대각선: $$1, 1, 1, 1, \dots$$ (모두 1)
- 두 번째 대각선: $$1, 2, 3, 4, \dots$$ (자연수)
- 세 번째 대각선: $$1, 3, 6, 10, \dots$$ (삼각수!)

<br>
세 번째 대각선의 수들은 $$\binom{n}{2} = \frac{n(n-1)}{2}$$로, 이는 삼각수와 밀접한 관련이 있습니다.

> 참고 : [자연수의 합 공식과 삼각수 - soo:bak](https://soo-bak.github.io/algorithm/theory/TriNum/)

<br>

#### 동적 계획법 구현

파스칼의 삼각형 성질을 그대로 코드로 구현하면 다음과 같습니다:

```cpp
#include <bits/stdc++.h>
using namespace std;

int dp[1001][1001];

int combination(int n, int r) {
  // 기저 조건
  if (r == 0 || r == n) return 1;
  
  // 이미 계산된 값이면 반환 (메모이제이션)
  if (dp[n][r] != 0) return dp[n][r];
  
  // 파스칼의 삼각형 성질 활용
  return dp[n][r] = combination(n - 1, r - 1) + combination(n - 1, r);
}
```

<br>
이 방식은 중복 계산을 제거하여 효율성을 크게 향상시킵니다.

시간 복잡도: $$O(n \times r)$$

공간 복잡도: $$O(n \times r)$$

<br>

---

## 조합 생성

조합의 개수를 계산하는 것뿐만 아니라, **실제로 가능한 모든 조합을 생성**해야 하는 경우가 많습니다.

예를 들어, 로또 번호를 선택하거나 특정 조건을 만족하는 조합을 찾는 문제에서는 모든 조합을 직접 생성해야 합니다.

<br>

### 재귀를 이용한 조합 생성

조합 생성의 가장 기본적인 방법은 재귀 함수를 활용하는 것입니다.

<br>
**핵심 아이디어**는 다음과 같습니다:

1. 현재 위치에서 하나의 원소를 선택합니다.
2. 다음 위치부터 나머지 원소들을 선택하도록 재귀 호출합니다.
3. $$r$$개를 모두 선택했다면 하나의 조합이 완성됩니다.
4. 선택을 취소하고 다음 원소로 넘어갑니다.

<br>
이 과정에서 **이미 선택한 원소보다 뒤에 있는 원소만을 대상**으로 하므로,

자연스럽게 중복 없이 순서를 고려하지 않는 조합이 생성됩니다.

<br>

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> combination;
vector<vector<int>> result;

void generateCombination(vector<int>& arr, int start, int r) {
  // 기저 조건: r개를 모두 선택했을 때
  if (combination.size() == r) {
    result.push_back(combination);
    return;
  }
  
  // start부터 끝까지 순회하며 원소 선택
  for (int i = start; i < arr.size(); i++) {
    combination.push_back(arr[i]);           // 원소 선택
    generateCombination(arr, i + 1, r);      // 다음 위치부터 재귀 호출
    combination.pop_back();                   // 선택 취소 (백트래킹)
  }
}

int main() {
  vector<int> arr = {1, 2, 3, 4, 5};
  int r = 3;
  
  generateCombination(arr, 0, r);
  
  cout << "가능한 조합의 개수: " << result.size() << "\n\n";
  
  for (auto& comb : result) {
    for (int num : comb) {
      cout << num << " ";
    }
    cout << "\n";
  }
  
  return 0;
}
```

<br>
위 코드에서 `start` 매개변수가 중요한 역할을 합니다.

이전에 선택한 원소의 다음 위치부터 탐색을 시작함으로써,

같은 조합이 중복해서 생성되는 것을 방지할 수 있습니다.

<br>

### 백트래킹을 이용한 조합 생성

백트래킹은 조합 생성의 대표적인 방법으로, 위의 재귀 방식과 본질적으로 동일합니다.

<br>
백트래킹의 핵심은 **선택과 취소를 반복**하며 모든 경우를 탐색하되,

불필요한 경로는 조기에 차단하여 효율성을 높이는 것입니다.

<br>

```cpp
#include <bits/stdc++.h>
using namespace std;

void backtrack(vector<int>& arr, vector<int>& comb, int start, int r) {
  // 기저 조건: r개를 모두 선택했을 때
  if (comb.size() == r) {
    for (int num : comb) {
      cout << num << " ";
    }
    cout << "\n";
    return;
  }
  
  // 현재 위치부터 끝까지 순회
  for (int i = start; i < arr.size(); i++) {
    comb.push_back(arr[i]);           // 선택
    backtrack(arr, comb, i + 1, r);   // 재귀 탐색
    comb.pop_back();                   // 선택 취소
  }
}

int main() {
  vector<int> arr = {1, 2, 3, 4};
  vector<int> comb;
  int r = 2;
  
  backtrack(arr, comb, 0, r);
  
  return 0;
}
```

<br>
조합 생성 과정은 **트리 구조**로 이해할 수 있습니다.

예를 들어, `{1, 2, 3}`에서 2개를 선택하는 경우:

```
                []
       /         |        \
      [1]       [2]       [3]
     /   \       |
   [1,2] [1,3]  [2,3]
```

각 레벨에서 하나씩 원소를 선택하고, 깊이가 $$r$$에 도달하면 하나의 조합이 완성됩니다.

<br>

> 참고 : [백트래킹(Backtracking)의 개념과 구조적 사고 - soo:bak](https://soo-bak.github.io/algorithm/theory/backTracking/)

<br>

---

## 시간 복잡도

### 조합의 개수 계산

- **팩토리얼 방식**: $$O(n)$$
- **동적 계획법 방식**: $$O(n \times r)$$

<br>

### 조합 생성

$$n$$개 중 $$r$$개를 선택하는 모든 조합을 생성하는 경우:

$$
O\left(\binom{n}{r} \times r\right)
$$

<br>
이는 생성할 조합의 개수 $$\binom{n}{r}$$에 각 조합을 출력하는 시간 $$r$$을 곱한 값입니다.

<br>

---

## 조합의 활용

조합은 알고리즘 문제뿐만 아니라 다양한 분야에서 핵심적으로 사용되는 개념입니다.

<br>

### 부분 집합 선택 문제

전체 집합에서 특정 개수의 원소를 선택하는 문제는 조합의 가장 직접적인 응용입니다.

<br>
예를 들어, $$n$$명의 학생 중 $$r$$명을 선발하는 경우의 수를 구하거나,

주어진 카드 중 몇 장을 선택하여 특정 조건을 만족시키는 문제 등이 이에 해당합니다.

<br>
이러한 문제에서는 조합의 개수를 계산하거나, 실제 조합을 생성하여 각 조합이 조건을 만족하는지 확인해야 합니다.

<br>

### 조합 최적화 문제

조합을 생성하면서 특정 기준에 따라 최적의 조합을 찾는 문제도 자주 등장합니다.

<br>
예를 들어, 배낭 문제(Knapsack Problem)에서는 무게 제한이 있는 배낭에 최대 가치를 담을 수 있도록

물건들의 조합을 선택해야 합니다.

<br>
또한, 여행 경로 최적화, 작업 스케줄링, 자원 배분 등의 문제에서도

가능한 조합 중 비용이 최소이거나 효율이 최대인 조합을 찾는 것이 목표가 됩니다.

<br>

### 확률과 통계

조합론은 확률 계산의 기초가 됩니다.

<br>
예를 들어, 52장의 카드에서 5장을 뽑을 때 특정 패턴이 나올 확률을 계산하려면

전체 가능한 조합의 개수 $$\binom{52}{5}$$와 원하는 패턴의 조합 개수를 알아야 합니다.

<br>
이처럼 확률은 **특정 사건의 경우의 수 / 전체 경우의 수**로 계산되므로,

조합의 개수를 정확히 구하는 것이 확률 계산의 핵심입니다.

<br>

### 이항 계수와 수학적 응용

조합의 개수 $$\binom{n}{r}$$은 **이항 계수(Binomial Coefficient)** 라고도 불립니다.

<br>
이항 계수는 **이항 정리(Binomial Theorem)** 에서 핵심적인 역할을 합니다:

$$
(x + y)^n = \sum_{r=0}^{n} \binom{n}{r} x^{n-r} y^r
$$

<br>
예를 들어, $$(x + y)^3$$을 전개하면:

$$
(x + y)^3 = \binom{3}{0}x^3 + \binom{3}{1}x^2y + \binom{3}{2}xy^2 + \binom{3}{3}y^3 = x^3 + 3x^2y + 3xy^2 + y^3
$$

<br>
여기서 계수 $$1, 3, 3, 1$$은 파스칼의 삼각형의 3번째 행과 정확히 일치합니다.

<br>
앞서 설명한 파스칼의 삼각형은 이항 계수를 시각적으로 배열한 것으로,

각 항이 위의 두 항의 합 $$\binom{n}{r} = \binom{n-1}{r-1} + \binom{n-1}{r}$$으로 구성됩니다.

<br>
이러한 수학적 성질은 조합론뿐만 아니라 대수학, 해석학, 확률론 등

다양한 수학 분야의 기초가 되며, 알고리즘 문제 해결에서도 중요하게 활용됩니다.

<br>

---

## 예제: 로또 번호 생성

6개의 번호를 선택하는 모든 조합을 생성하는 예제입니다.

```cpp
#include <bits/stdc++.h>
using namespace std;

void generateLotto(vector<int>& numbers, vector<int>& selected, int start) {
  if (selected.size() == 6) {
    for (int i = 0; i < 6; i++) {
      cout << selected[i];
      if (i < 5) cout << " ";
    }
    cout << "\n";
    return;
  }
  
  for (int i = start; i < numbers.size(); i++) {
    selected.push_back(numbers[i]);
    generateLotto(numbers, selected, i + 1);
    selected.pop_back();
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  
  int k;
  while (cin >> k && k != 0) {
    vector<int> numbers(k);
    for (int i = 0; i < k; i++) {
      cin >> numbers[i];
    }
    
    vector<int> selected;
    generateLotto(numbers, selected, 0);
    cout << "\n";
  }
  
  return 0;
}
```

<br>

---

## 중복 조합

**중복 조합(Combination with Repetition)** 은 같은 원소를 중복해서 선택할 수 있는 조합입니다.

<br>
일반 조합과 달리, 중복 조합에서는 한 원소를 여러 번 선택할 수 있습니다.

예를 들어, 과일 가게에서 사과, 배, 오렌지 중 3개를 선택한다고 할 때,

같은 과일을 여러 개 선택할 수 있다면 이는 중복 조합 문제가 됩니다.

<br>

### 중복 조합의 개수

$$n$$개 중 $$r$$개를 중복을 허용하여 선택하는 중복 조합의 개수는:

$$
H(n, r) = \binom{n+r-1}{r} = \frac{(n+r-1)!}{r!(n-1)!}
$$

<br>
이 공식은 언뜻 복잡해 보이지만, **막대와 칸막이 방법(Stars and Bars Method)** 을 통해 직관적으로 이해할 수 있습니다.

<br>

#### 막대와 칸막이 방법의 원리

$$n$$종류의 원소 중 $$r$$개를 중복 선택하는 문제를 다음과 같이 생각해봅시다.

<br>
$$r$$개의 막대(★)와 $$(n-1)$$개의 칸막이(|)를 일렬로 배치하는 것으로 치환할 수 있습니다.

- 칸막이는 $$n$$종류의 원소를 구분하는 역할을 합니다.
- 각 구역에 있는 막대의 개수가 해당 원소를 선택한 횟수를 나타냅니다.

<br>
예를 들어, 3종류의 과일 중 5개를 중복 선택하는 경우를 생각해봅시다.

`★★|★|★★` 라는 배치는:
- 첫 번째 과일: 2개 (★★)
- 두 번째 과일: 1개 (★)
- 세 번째 과일: 2개 (★★)

를 의미합니다.

<br>
따라서 문제는 총 $$(r + n - 1)$$개의 위치 중에서 $$r$$개의 막대를 놓을 위치를 선택하는 문제가 됩니다.

이는 $$(r + n - 1)$$개 중 $$r$$개를 선택하는 조합이므로:

$$
H(n, r) = \binom{n+r-1}{r}
$$

<br>
또는 칸막이 $$(n-1)$$개를 놓을 위치를 선택하는 관점에서 보면:

$$
H(n, r) = \binom{n+r-1}{n-1}
$$

<br>

### 중복 조합 생성 구현

중복 조합은 일반 조합과 유사하게 백트래킹으로 생성할 수 있습니다.

차이점은 재귀 호출 시 `i + 1`이 아닌 `i`를 전달하여 같은 원소를 다시 선택할 수 있도록 한다는 것입니다.

<br>

```cpp
#include <bits/stdc++.h>
using namespace std;

void generateCombWithRep(vector<int>& arr, vector<int>& selected, int start, int r) {
  // 기저 조건: r개를 모두 선택했을 때
  if (selected.size() == r) {
    for (int num : selected) {
      cout << num << " ";
    }
    cout << "\n";
    return;
  }
  
  // start부터 끝까지 순회 (같은 원소 재선택 가능)
  for (int i = start; i < arr.size(); i++) {
    selected.push_back(arr[i]);
    generateCombWithRep(arr, selected, i, r);  // i를 전달 (중복 허용)
    selected.pop_back();
  }
}

int main() {
  vector<int> arr = {1, 2, 3};
  vector<int> selected;
  int r = 2;
  
  cout << "중복 조합:\n";
  generateCombWithRep(arr, selected, 0, r);
  
  return 0;
}
```

<br>
위 코드에서 `{1, 2, 3}` 중 2개를 중복 선택하면 다음과 같은 조합이 생성됩니다:

```
1 1
1 2
1 3
2 2
2 3
3 3
```

일반 조합에서는 `{1, 1}`, `{2, 2}`, `{3, 3}` 같은 경우가 불가능하지만,

중복 조합에서는 같은 원소를 여러 번 선택할 수 있습니다.

<br>

---

## 마무리

조합은 $$n$$개 중 $$r$$개를 순서 없이 선택하는 경우의 수로,

알고리즘 문제 해결의 기본이 되는 중요한 개념입니다.

<br>
조합의 개수를 계산하는 방법으로는 팩토리얼을 직접 사용하는 방법과

파스칼의 삼각형 성질을 활용한 동적 계획법이 있으며,

실제 조합을 생성할 때는 재귀와 백트래킹을 통해 구현합니다.

<br>
조합론은 순열, 중복 순열, 중복 조합 등으로 확장되며,

각각이 서로 다른 문제 상황에 적용됩니다.

<br>
특히 조합은 부분 집합 선택, 최적화 문제, 확률 계산, 이항 정리 등

다양한 수학적·실용적 문제에서 핵심적인 역할을 하므로,

그 원리와 구현 방법을 정확히 이해하는 것이 중요합니다.

<br>

**관련 문제**:
- [백준 6603번 - 로또](https://soo-bak.github.io/algorithm/boj/lotto-combination-35/)
- [백준 2529번 - 부등호](https://soo-bak.github.io/algorithm/boj/inequality-signs-03/)


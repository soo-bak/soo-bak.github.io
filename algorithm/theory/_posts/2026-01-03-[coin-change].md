---
layout: single
title: "동전 교환(Coin Change) 문제의 원리와 구현 - soo:bak"
date: "2026-01-03 15:00:00 +0900"
description: 동적 계획법을 활용한 동전 교환 문제의 두 가지 변형(최소 개수, 경우의 수)과 구현 방법을 다룹니다
---

## 동전 교환 문제란?

**동전 교환(Coin Change)** 문제는 주어진 동전들로 특정 금액을 만드는 방법을 찾는 문제입니다.

<br>

두 가지 주요 변형이 있습니다:

1. **최소 개수**: 금액을 만드는 데 필요한 **최소 동전 개수**
2. **경우의 수**: 금액을 만드는 **가능한 조합의 수**

<br>

**예시**

동전: `[1, 2, 5]`, 금액: `11`

- 최소 개수: 3개 (5 + 5 + 1)
- 경우의 수: 11가지

<br>

## 문제 1: 최소 동전 개수

<br>

### DP 점화식

$$dp[i]$$: 금액 $$i$$를 만드는 데 필요한 최소 동전 개수

$$
dp[i] = \min_{c \in \text{coins}}(dp[i - c]) + 1
$$

<br>

### 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

int coinChangeMin(vector<int>& coins, int amount) {
  vector<int> dp(amount + 1, INT_MAX);
  dp[0] = 0;

  for (int i = 1; i <= amount; i++) {
    for (int coin : coins) {
      if (coin <= i && dp[i - coin] != INT_MAX) {
        dp[i] = min(dp[i], dp[i - coin] + 1);
      }
    }
  }

  return dp[amount] == INT_MAX ? -1 : dp[amount];
}

int main() {
  vector<int> coins = {1, 2, 5};
  int amount = 11;

  cout << coinChangeMin(coins, amount) << "\n";  // 3

  return 0;
}
```

<br>

### DP 테이블 예시

동전 `[1, 2, 5]`, 금액 `11`:

```
금액:  0  1  2  3  4  5  6  7  8  9  10  11
dp:   0  1  1  2  2  1  2  2  3  3   2   3
```

- $$dp[5] = 1$$ (동전 5 하나)
- $$dp[11] = 3$$ (5 + 5 + 1)

<br>

### 사용된 동전 역추적

```cpp
vector<int> getCoins(vector<int>& coins, int amount) {
  vector<int> dp(amount + 1, INT_MAX);
  vector<int> parent(amount + 1, -1);
  dp[0] = 0;

  for (int i = 1; i <= amount; i++) {
    for (int coin : coins) {
      if (coin <= i && dp[i - coin] != INT_MAX) {
        if (dp[i - coin] + 1 < dp[i]) {
          dp[i] = dp[i - coin] + 1;
          parent[i] = coin;
        }
      }
    }
  }

  vector<int> result;
  if (dp[amount] == INT_MAX) return result;

  int curr = amount;
  while (curr > 0) {
    result.push_back(parent[curr]);
    curr -= parent[curr];
  }

  return result;
}
```

<br>

## 문제 2: 경우의 수

<br>

### 순서 구분 없는 경우 (조합)

같은 동전 조합은 한 번만 셉니다: `[1,2]`와 `[2,1]`은 같은 것

<br>

**DP 점화식**

$$dp[i]$$: 금액 $$i$$를 만드는 조합의 수

**핵심**: 동전을 순서대로 고려

```cpp
int coinChangeCombinations(vector<int>& coins, int amount) {
  vector<int> dp(amount + 1, 0);
  dp[0] = 1;

  for (int coin : coins) {
    for (int i = coin; i <= amount; i++) {
      dp[i] += dp[i - coin];
    }
  }

  return dp[amount];
}
```

<br>

### 순서 구분 있는 경우 (순열)

`[1,2]`와 `[2,1]`을 다른 것으로 셉니다.

```cpp
int coinChangePermutations(vector<int>& coins, int amount) {
  vector<int> dp(amount + 1, 0);
  dp[0] = 1;

  for (int i = 1; i <= amount; i++) {
    for (int coin : coins) {
      if (coin <= i) {
        dp[i] += dp[i - coin];
      }
    }
  }

  return dp[amount];
}
```

<br>

### 차이점 비교

동전 `[1, 2]`, 금액 `3`:

| 방식 | 결과 | 경우들 |
|------|------|--------|
| 조합 | 2 | [1,1,1], [1,2] |
| 순열 | 3 | [1,1,1], [1,2], [2,1] |

<br>

## 시간 복잡도

<br>

| 문제 | 시간 | 공간 |
|------|------|------|
| 최소 개수 | $$O(n \times m)$$ | $$O(n)$$ |
| 경우의 수 | $$O(n \times m)$$ | $$O(n)$$ |

여기서 $$n$$은 금액, $$m$$은 동전 종류 수입니다.

<br>

## 변형 문제

<br>

### 1. 동전 개수 제한

각 동전을 최대 $$k$$개만 사용할 수 있는 경우:

```cpp
int coinChangeLimit(vector<int>& coins, vector<int>& limits, int amount) {
  vector<int> dp(amount + 1, 0);
  dp[0] = 1;

  for (int i = 0; i < coins.size(); i++) {
    int coin = coins[i];
    int limit = limits[i];

    // 역순으로 순회 (각 동전을 limit개까지만)
    for (int j = amount; j >= coin; j--) {
      for (int k = 1; k <= limit && k * coin <= j; k++) {
        dp[j] += dp[j - k * coin];
      }
    }
  }

  return dp[amount];
}
```

<br>

### 2. 정확히 k개 사용

```cpp
int coinChangeExactK(vector<int>& coins, int amount, int k) {
  // dp[i][j]: j개의 동전으로 금액 i를 만드는 경우의 수
  vector<vector<int>> dp(amount + 1, vector<int>(k + 1, 0));
  dp[0][0] = 1;

  for (int coin : coins) {
    for (int i = coin; i <= amount; i++) {
      for (int j = 1; j <= k; j++) {
        dp[i][j] += dp[i - coin][j - 1];
      }
    }
  }

  return dp[amount][k];
}
```

<br>

### 3. 무한 배낭과의 관계

동전 교환의 "경우의 수" 문제는 **무한 배낭 문제**의 특수 케이스입니다.

- 동전 = 물건
- 금액 = 배낭 용량
- 모든 동전의 가치 = 1

<br>

## 그리디 vs DP

<br>

**그리디가 되는 경우**

동전이 **정규 시스템**(canonical system)일 때:
- 예: [1, 5, 10, 50, 100, 500] (한국 동전)
- 큰 동전부터 선택하면 최적해

<br>

**그리디가 안 되는 경우**

```
동전: [1, 3, 4]
금액: 6

그리디: 4 + 1 + 1 = 3개
최적해: 3 + 3 = 2개
```

<br>

**결론**: 일반적인 경우 DP를 사용해야 합니다.

<br>

## 실전 팁

<br>

**1. 조합 vs 순열 구분**

```cpp
// 조합: 동전 기준 외부 루프
for (coin : coins)
  for (i : amounts)

// 순열: 금액 기준 외부 루프
for (i : amounts)
  for (coin : coins)
```

<br>

**2. 불가능한 경우 처리**

```cpp
// 최소 개수: INT_MAX 또는 -1 반환
if (dp[amount] == INT_MAX) return -1;

// 경우의 수: 0 반환 (자연스럽게 처리됨)
```

<br>

**3. MOD 연산**

경우의 수가 클 때:

```cpp
const int MOD = 1e9 + 7;
dp[i] = (dp[i] + dp[i - coin]) % MOD;
```

<br>

## 마무리

동전 교환 문제는 DP의 대표적인 응용으로, 배낭 문제와 밀접한 관련이 있습니다.

<br>

**핵심 포인트**
- **최소 개수**: $$\min(dp[i-c]) + 1$$
- **경우의 수 (조합)**: 동전별로 순차 처리
- **경우의 수 (순열)**: 금액별로 모든 동전 시도
- **시간 복잡도**: $$O(n \times m)$$

<br>

### 관련 글
- [동적 계획법(Dynamic Programming) - soo:bak](https://soo-bak.github.io/algorithm/theory/dynamic-programming/)
- [배낭 문제(Knapsack Problem) - soo:bak](https://soo-bak.github.io/algorithm/theory/knapsack/)

<br>

### 관련 문제
- [[백준 2293] 동전 1](https://www.acmicpc.net/problem/2293)
- [[백준 2294] 동전 2](https://www.acmicpc.net/problem/2294)


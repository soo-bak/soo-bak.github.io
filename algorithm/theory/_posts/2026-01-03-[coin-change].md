---
layout: single
title: "동전 교환(Coin Change) 문제의 원리와 구현 - soo:bak"
date: "2026-01-03 15:00:00 +0900"
description: 동적 계획법을 활용한 동전 교환 문제의 두 가지 변형(최소 개수, 경우의 수)과 구현 방법을 다룹니다
---

## 동전 교환 문제란?

**동전 교환(Coin Change)** 문제는 주어진 동전들로 특정 금액을 만드는 방법을 찾는 문제입니다.

<br>
이 문제에는 두 가지 주요 변형이 있습니다:

<br>

**1. 최소 개수 문제**

금액을 만드는 데 필요한 최소 동전 개수를 구합니다.

<br>

**2. 경우의 수 문제**

금액을 만드는 가능한 조합의 수를 구합니다.

<br>
예를 들어, 동전이 `[1, 2, 5]`이고 금액이 `11`일 때:

- 최소 개수: 3개 (5 + 5 + 1)
- 경우의 수: 11가지

<br>

---

<br>

## 최소 동전 개수

금액 $$i$$를 만드는 데 필요한 최소 동전 개수를 $$dp[i]$$라고 정의합니다.

<br>
각 동전 $$c$$에 대해, $$i - c$$ 금액을 만들 수 있다면 거기에 동전 하나를 추가하면 됩니다.

<br>

**점화식**:

$$
dp[i] = \min_{c \in \text{coins}}(dp[i - c]) + 1
$$

<br>

**기저 조건**:
$$
dp[0] = 0 \quad \text{(금액 0을 만드는 데 필요한 동전은 0개)}
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
동전 `[1, 2, 5]`로 금액 `11`을 만들 때 $$dp$$ 배열의 변화:

```
금액:  0  1  2  3  4  5  6  7  8  9  10  11
dp:   0  1  1  2  2  1  2  2  3  3   2   3
```

<br>
$$dp[5] = 1$$은 동전 5 하나로 금액 5를 만들 수 있음을 의미하고,

$$dp[11] = 3$$은 5 + 5 + 1로 금액 11을 만들 수 있음을 의미합니다.

<br>

### 사용된 동전 역추적

최소 개수뿐 아니라 어떤 동전을 사용했는지 알고 싶다면,

각 금액에서 선택한 동전을 별도 배열에 저장해두면 됩니다.

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

---

<br>

## 경우의 수

금액을 만드는 경우의 수를 구할 때는 순서를 구분하는지 여부에 따라 두 가지로 나뉩니다.

<br>

### 순서 구분 없는 경우 (조합)

`[1, 2]`와 `[2, 1]`을 같은 것으로 셉니다.

<br>
중복을 피하기 위해 동전을 순서대로 고려합니다.

한 동전에 대해 모든 금액을 처리한 후, 다음 동전으로 넘어갑니다.

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

`[1, 2]`와 `[2, 1]`을 다른 것으로 셉니다.

<br>
각 금액에서 모든 동전을 시도합니다.

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
동전 `[1, 2]`로 금액 `3`을 만드는 경우:

- 조합: 2가지 ([1,1,1], [1,2])
- 순열: 3가지 ([1,1,1], [1,2], [2,1])

<br>
루프 순서가 결과를 결정합니다.

동전이 바깥 루프면 조합, 금액이 바깥 루프면 순열입니다.

<br>

---

<br>

## 시간 복잡도와 공간 복잡도

최소 개수 문제와 경우의 수 문제 모두 시간 복잡도는 $$O(n \times m)$$입니다.

여기서 $$n$$은 금액, $$m$$은 동전 종류 수입니다.

<br>
공간 복잡도는 $$O(n)$$으로, 금액만큼의 1차원 배열이 필요합니다.

<br>

---

<br>

## 변형 문제

<br>

### 동전 개수 제한

각 동전을 최대 $$k$$개만 사용할 수 있는 경우입니다.

<br>
0/1 배낭 문제처럼 역순으로 순회하여 같은 동전을 중복 사용하지 않도록 합니다.

```cpp
int coinChangeLimit(vector<int>& coins, vector<int>& limits, int amount) {
  vector<int> dp(amount + 1, 0);
  dp[0] = 1;

  for (int i = 0; i < coins.size(); i++) {
    int coin = coins[i];
    int limit = limits[i];

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

### 정확히 k개 사용

정확히 $$k$$개의 동전으로 금액을 만드는 경우입니다.

<br>
2차원 DP로 확장하여 동전 개수도 함께 추적합니다.

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

---

<br>

## 그리디와의 비교

동전 교환 문제에서 그리디 알고리듬이 항상 최적해를 보장하지는 않습니다.

<br>
한국의 동전 체계 `[1, 5, 10, 50, 100, 500]`처럼 큰 동전이 작은 동전의 배수인 경우에는

그리디로 큰 동전부터 선택해도 최적해를 얻을 수 있습니다.

<br>
하지만 동전이 `[1, 3, 4]`이고 금액이 `6`인 경우:

- 그리디: 4 + 1 + 1 = 3개
- 최적해: 3 + 3 = 2개

<br>
따라서 일반적인 경우에는 동적 계획법을 사용해야 합니다.

<br>

---

<br>

## 구현 시 주의사항

경우의 수가 매우 커질 수 있으므로, 문제에서 요구하는 경우 MOD 연산을 적용합니다.

```cpp
const int MOD = 1e9 + 7;
dp[i] = (dp[i] + dp[i - coin]) % MOD;
```

<br>
최소 개수 문제에서 금액을 만들 수 없는 경우, $$dp[amount]$$가 초기값 그대로이므로

이를 확인하여 `-1`이나 적절한 값을 반환합니다.

<br>

---

<br>

## 마무리

동전 교환 문제는 동적 계획법의 대표적인 응용 문제입니다.

<br>
최소 개수 문제는 각 금액에서 가능한 동전들 중 최솟값을 선택하고,

경우의 수 문제는 루프 순서에 따라 조합과 순열로 나뉩니다.

<br>
배낭 문제와 밀접한 관련이 있으며,

동전을 물건으로, 금액을 배낭 용량으로 생각하면 무한 배낭 문제의 특수 케이스로 볼 수 있습니다.

<br>

> 참고 : [동적 계획법(Dynamic Programming)의 원리와 설계 - soo:bak](https://soo-bak.github.io/algorithm/theory/dynamic-programming/)

<br>

**관련 문제**:
- [백준 2293번 - 동전 1](https://www.acmicpc.net/problem/2293)
- [백준 2294번 - 동전 2](https://www.acmicpc.net/problem/2294)


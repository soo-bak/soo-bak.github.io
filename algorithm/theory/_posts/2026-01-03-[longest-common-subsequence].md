---
layout: single
title: "최장 공통 부분 수열(LCS)의 원리와 구현 - soo:bak"
date: "2026-01-03 13:00:00 +0900"
description: 두 문자열에서 공통으로 나타나는 가장 긴 부분 수열을 찾는 LCS 알고리듬의 원리, DP 구현, 역추적 방법을 다룹니다
tags:
  - 다이나믹 프로그래밍
  - LCS
  - 문자열
---

## LCS란?

**최장 공통 부분 수열(Longest Common Subsequence, LCS)**은 두 수열에서 **공통으로 나타나는 가장 긴 부분 수열**을 찾는 문제입니다.

<br>
**부분 수열(Subsequence)**은 원래 수열에서 일부 원소를 삭제하여 얻은 수열입니다.

연속할 필요는 없지만 **순서는 유지**해야 합니다.

<br>
예를 들어, 두 문자열 `X = "ABCDGH"`와 `Y = "AEDFHR"`가 있다면,

공통으로 나타나면서 순서를 유지하는 가장 긴 부분 수열은 `"ADH"`이며 길이는 `3`입니다.

<br>

---

<br>

## 부분 수열과 부분 문자열의 차이

LCS 문제를 다룰 때 자주 혼동되는 개념이 있습니다.

<br>
**부분 수열(Subsequence)**은 원소들이 연속하지 않아도 되며, 원래 순서만 유지하면 됩니다.

반면 **부분 문자열(Substring)**은 원소들이 연속해야 합니다.

<br>
예를 들어, `"ABCD"`와 `"ACBD"`의 경우:

- 최장 공통 부분 수열(Subsequence)은 `"ABD"` (길이 3)
- 최장 공통 부분 문자열(Substring)은 `"A"` 또는 `"B"` (길이 1)

<br>
이 글에서는 **부분 수열(Subsequence)** 버전을 다룹니다.

<br>

---

<br>

## 동적 계획법으로 LCS 구하기

LCS 문제는 동적 계획법의 조건인 **최적 부분 구조**와 **중복 부분 문제**를 만족합니다.

<br>
두 문자열 $$X[1..m]$$과 $$Y[1..n]$$에 대해 $$dp[i][j]$$를 $$X[1..i]$$와 $$Y[1..j]$$의 LCS 길이로 정의합니다.

<br>

**점화식**:

$$
dp[i][j] = \begin{cases}
0 & \text{if } i = 0 \text{ or } j = 0 \\
dp[i-1][j-1] + 1 & \text{if } X[i] = Y[j] \\
\max(dp[i-1][j], dp[i][j-1]) & \text{if } X[i] \neq Y[j]
\end{cases}
$$

<br>
두 문자가 같으면 이전 LCS에 `1`을 더하고,

다르면 한쪽을 제외한 두 경우 중 더 큰 값을 선택합니다.

<br>

**기저 조건**:

$$dp[0][j] = 0$$, $$dp[i][0] = 0$$

빈 문자열과의 LCS는 항상 `0`입니다.

<br>

> 참고 : [동적 계획법(Dynamic Programming)의 원리와 설계 - soo:bak](https://soo-bak.github.io/algorithm/theory/dynamic-programming/)

<br>

---

<br>

## DP 테이블 채우기 예시

$$X = \text{"AGCAT"}$$, $$Y = \text{"GAC"}$$일 때 DP 테이블은 다음과 같이 채워집니다:

```
    ""  G  A  C
""   0  0  0  0
A    0  0  1  1
G    0  1  1  1
C    0  1  1  2
A    0  1  2  2
T    0  1  2  2
```

<br>
최종 답은 $$dp[5][3] = 2$$이며, LCS는 `"AC"` 또는 `"GC"`입니다.

<br>

---

<br>

## 구현

### 기본 구현 (길이만 구하기)

```cpp
#include <bits/stdc++.h>
using namespace std;

int lcsLength(const string& X, const string& Y) {
  int m = X.size(), n = Y.size();
  vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));

  for (int i = 1; i <= m; i++) {
    for (int j = 1; j <= n; j++) {
      if (X[i - 1] == Y[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  return dp[m][n];
}

int main() {
  string X = "AGCAT";
  string Y = "GAC";

  cout << "LCS 길이: " << lcsLength(X, Y) << "\n";  // 2

  return 0;
}
```

<br>
**시간 복잡도**: $$O(mn)$$

**공간 복잡도**: $$O(mn)$$

<br>

### LCS 문자열 역추적

LCS의 길이뿐 아니라 실제 문자열을 복원하려면 DP 테이블을 역으로 따라가야 합니다.

```cpp
#include <bits/stdc++.h>
using namespace std;

string lcs(const string& X, const string& Y) {
  int m = X.size(), n = Y.size();
  vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));

  // DP 테이블 채우기
  for (int i = 1; i <= m; i++) {
    for (int j = 1; j <= n; j++) {
      if (X[i - 1] == Y[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  // 역추적으로 LCS 문자열 복원
  string result;
  int i = m, j = n;

  while (i > 0 && j > 0) {
    if (X[i - 1] == Y[j - 1]) {
      result = X[i - 1] + result;
      i--;
      j--;
    } else if (dp[i - 1][j] > dp[i][j - 1]) {
      i--;
    } else {
      j--;
    }
  }

  return result;
}

int main() {
  string X = "ABCDGH";
  string Y = "AEDFHR";

  cout << "LCS: " << lcs(X, Y) << "\n";  // ADH

  return 0;
}
```

<br>
역추적 과정에서 두 문자가 같으면 해당 문자를 결과에 추가하고,

다르면 DP 값이 더 큰 쪽으로 이동합니다.

<br>

---

<br>

## 공간 최적화

LCS 길이만 필요하고 역추적이 불필요한 경우,

현재 행과 이전 행만 유지하면 공간을 $$O(n)$$으로 줄일 수 있습니다.

```cpp
int lcsLengthOptimized(const string& X, const string& Y) {
  int m = X.size(), n = Y.size();
  vector<int> prev(n + 1, 0), curr(n + 1, 0);

  for (int i = 1; i <= m; i++) {
    for (int j = 1; j <= n; j++) {
      if (X[i - 1] == Y[j - 1]) {
        curr[j] = prev[j - 1] + 1;
      } else {
        curr[j] = max(prev[j], curr[j - 1]);
      }
    }
    swap(prev, curr);
  }

  return prev[n];
}
```

<br>
다만 공간 최적화를 적용하면 역추적이 불가능해집니다.

실제 LCS 문자열이 필요한 경우 2차원 테이블을 유지해야 합니다.

<br>

---

<br>

## LCS의 변형 문제

### 1. 최장 공통 부분 문자열 (Substring)

연속해야 하는 버전입니다. 문자가 다르면 `0`으로 초기화됩니다.

```cpp
int lcsSubstring(const string& X, const string& Y) {
  int m = X.size(), n = Y.size();
  vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
  int maxLen = 0;

  for (int i = 1; i <= m; i++) {
    for (int j = 1; j <= n; j++) {
      if (X[i - 1] == Y[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
        maxLen = max(maxLen, dp[i][j]);
      }
      // 다르면 0 (연속 끊김)
    }
  }

  return maxLen;
}
```

<br>

### 2. 세 문자열의 LCS

3차원 DP 테이블을 사용합니다.

```cpp
int lcs3(const string& X, const string& Y, const string& Z) {
  int l = X.size(), m = Y.size(), n = Z.size();
  vector<vector<vector<int>>> dp(l + 1,
    vector<vector<int>>(m + 1, vector<int>(n + 1, 0)));

  for (int i = 1; i <= l; i++) {
    for (int j = 1; j <= m; j++) {
      for (int k = 1; k <= n; k++) {
        if (X[i - 1] == Y[j - 1] && Y[j - 1] == Z[k - 1]) {
          dp[i][j][k] = dp[i - 1][j - 1][k - 1] + 1;
        } else {
          dp[i][j][k] = max({dp[i - 1][j][k],
                            dp[i][j - 1][k],
                            dp[i][j][k - 1]});
        }
      }
    }
  }

  return dp[l][m][n];
}
```

<br>

---

<br>

## 활용 예시

**diff 도구**: 파일 비교 시 변경되지 않은 부분(공통 부분)을 찾는 데 사용됩니다.

<br>
**DNA 서열 비교**: 두 DNA 서열의 유사도를 측정할 때 활용됩니다.

<br>
**편집 거리와의 관계**: 두 문자열의 편집 거리는 LCS를 이용해 계산할 수 있습니다.

$$\text{편집 거리} = m + n - 2 \times \text{LCS 길이}$$

<br>

---

<br>

## 마무리

최장 공통 부분 수열(LCS)은 두 수열에서 순서를 유지하며 공통으로 나타나는 가장 긴 수열을 찾는 문제입니다.

<br>
동적 계획법을 적용하여 $$O(mn)$$ 시간에 해결할 수 있으며,

DP 테이블을 역추적하면 실제 LCS 문자열도 복원할 수 있습니다.

<br>

> 참고 : [동적 계획법(Dynamic Programming)의 원리와 설계 - soo:bak](https://soo-bak.github.io/algorithm/theory/dynamic-programming/)

<br>

**관련 문제**:
- [백준 9251번 - LCS](https://www.acmicpc.net/problem/9251)
- [백준 9252번 - LCS 2](https://www.acmicpc.net/problem/9252)

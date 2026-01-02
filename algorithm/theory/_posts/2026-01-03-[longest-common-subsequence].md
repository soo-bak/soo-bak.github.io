---
layout: single
title: "최장 공통 부분 수열(LCS)의 원리와 구현 - soo:bak"
date: "2026-01-03 13:00:00 +0900"
description: 두 문자열에서 공통으로 나타나는 가장 긴 부분 수열을 찾는 LCS 알고리듬의 원리, DP 구현, 역추적 방법을 다룹니다
---

## LCS란?

**최장 공통 부분 수열(Longest Common Subsequence, LCS)**은 두 수열에서 **공통으로 나타나는 가장 긴 부분 수열**을 찾는 문제입니다.

<br>

**부분 수열(Subsequence)**은 원래 수열에서 일부 원소를 삭제하여 얻은 수열입니다.

연속할 필요는 없지만 **순서는 유지**해야 합니다.

<br>

**예시**

```
X = "ABCDGH"
Y = "AEDFHR"

LCS = "ADH" (길이 3)
```

<br>

## LCS vs LCS (Substring)

<br>

| 개념 | 설명 | 예시 |
|------|------|------|
| LCS (Subsequence) | 순서만 유지, 연속 불필요 | "ABCD"와 "ACBD" → "ABD" |
| LCS (Substring) | 연속해야 함 | "ABCD"와 "BCDE" → "BCD" |

<br>

이 글에서는 **부분 수열(Subsequence)** 버전을 다룹니다.

<br>

## DP 점화식

<br>

두 문자열 $$X[1..m]$$과 $$Y[1..n]$$에 대해:

$$
dp[i][j] = \begin{cases}
0 & \text{if } i = 0 \text{ or } j = 0 \\
dp[i-1][j-1] + 1 & \text{if } X[i] = Y[j] \\
\max(dp[i-1][j], dp[i][j-1]) & \text{if } X[i] \neq Y[j]
\end{cases}
$$

<br>

**의미**:
- $$dp[i][j]$$: $$X[1..i]$$와 $$Y[1..j]$$의 LCS 길이
- 문자가 같으면: 이전 LCS에 1을 더함
- 문자가 다르면: 둘 중 하나를 제외한 최댓값

<br>

## DP 테이블 예시

<br>

$$X = \text{"AGCAT"}$$, $$Y = \text{"GAC"}$$

```
    ""  G  A  C
""   0  0  0  0
A    0  0  1  1
G    0  1  1  1
C    0  1  1  2
A    0  1  2  2
T    0  1  2  2
```

**LCS 길이**: $$dp[5][3] = 2$$ (예: "AC" 또는 "GC")

<br>

## LCS 구현

<br>

### 기본 구현 (길이만)

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

### LCS 문자열 역추적

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

### 공간 최적화 (길이만)

$$O(n)$$ 공간으로 길이만 구하기:

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

## 시간 복잡도

<br>

| 방법 | 시간 | 공간 |
|------|------|------|
| 기본 DP | $$O(mn)$$ | $$O(mn)$$ |
| 공간 최적화 | $$O(mn)$$ | $$O(n)$$ |
| 역추적 포함 | $$O(mn)$$ | $$O(mn)$$ |

<br>

## LCS 변형 문제

<br>

### 1. 최장 공통 부분 문자열 (Substring)

연속해야 하는 버전:

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

### 3. LCS 개수 세기

서로 다른 LCS의 개수:

```cpp
pair<int, int> lcsWithCount(const string& X, const string& Y) {
  int m = X.size(), n = Y.size();
  vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
  vector<vector<int>> cnt(m + 1, vector<int>(n + 1, 1));

  for (int i = 1; i <= m; i++) {
    for (int j = 1; j <= n; j++) {
      if (X[i - 1] == Y[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
        cnt[i][j] = cnt[i - 1][j - 1];
      } else if (dp[i - 1][j] > dp[i][j - 1]) {
        dp[i][j] = dp[i - 1][j];
        cnt[i][j] = cnt[i - 1][j];
      } else if (dp[i - 1][j] < dp[i][j - 1]) {
        dp[i][j] = dp[i][j - 1];
        cnt[i][j] = cnt[i][j - 1];
      } else {
        dp[i][j] = dp[i - 1][j];
        cnt[i][j] = cnt[i - 1][j] + cnt[i][j - 1];
        if (dp[i - 1][j - 1] == dp[i][j]) {
          cnt[i][j] -= cnt[i - 1][j - 1];
        }
      }
    }
  }

  return {dp[m][n], cnt[m][n]};
}
```

<br>

## 활용 예시

<br>

**1. diff 도구**

파일 비교 시 변경되지 않은 부분(공통 부분)을 찾습니다.

<br>

**2. DNA 서열 비교**

두 DNA 서열의 유사도를 측정합니다.

<br>

**3. 편집 거리와의 관계**

$$\text{편집 거리} = m + n - 2 \times \text{LCS 길이}$$

<br>

## 마무리

최장 공통 부분 수열(LCS)은 두 수열의 공통 구조를 찾는 기본적인 DP 문제입니다.

<br>

**핵심 포인트**
- **정의**: 순서를 유지하며 공통으로 나타나는 가장 긴 수열
- **점화식**: 문자 일치 시 $$+1$$, 불일치 시 $$\max$$
- **시간 복잡도**: $$O(mn)$$
- **역추적**: DP 테이블을 역으로 따라가며 복원

<br>

### 관련 글
- [동적 계획법(Dynamic Programming) - soo:bak](https://soo-bak.github.io/algorithm/theory/dynamic-programming/)

<br>

### 관련 문제
- [[백준 9251] LCS](https://www.acmicpc.net/problem/9251)
- [[백준 9252] LCS 2](https://www.acmicpc.net/problem/9252)


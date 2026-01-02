---
layout: single
title: "모듈러 연산(Modular Arithmetic)의 원리와 활용 - soo:bak"
date: "2026-01-03 14:00:00 +0900"
description: 나머지 연산의 성질, 모듈러 덧셈/뺄셈/곱셈, 거듭제곱, 역원 계산 방법을 다룹니다
---

## 모듈러 연산이란?

**모듈러 연산(Modular Arithmetic)**은 나머지 연산을 체계적으로 다루는 수학 분야입니다.

<br>

$$a \equiv b \pmod{m}$$

$$a$$를 $$m$$으로 나눈 나머지가 $$b$$와 같다는 의미입니다.

<br>

**예시**:
- $$17 \equiv 2 \pmod{5}$$ (17 = 5×3 + 2)
- $$-3 \equiv 4 \pmod{7}$$ (-3 = 7×(-1) + 4)

<br>

## 기본 연산

<br>

### 덧셈

$$(a + b) \mod m = ((a \mod m) + (b \mod m)) \mod m$$

```cpp
long long modAdd(long long a, long long b, long long m) {
  return ((a % m) + (b % m)) % m;
}
```

<br>

### 뺄셈

$$(a - b) \mod m = ((a \mod m) - (b \mod m) + m) \mod m$$

```cpp
long long modSub(long long a, long long b, long long m) {
  return ((a % m) - (b % m) + m) % m;
}
```

**주의**: 음수가 될 수 있으므로 $$+m$$을 더합니다.

<br>

### 곱셈

$$(a \times b) \mod m = ((a \mod m) \times (b \mod m)) \mod m$$

```cpp
long long modMul(long long a, long long b, long long m) {
  return ((a % m) * (b % m)) % m;
}
```

**주의**: 오버플로우 방지를 위해 `long long` 사용

<br>

## 모듈러 거듭제곱

<br>

$$a^n \mod m$$을 효율적으로 계산하는 방법입니다.

### 분할 정복 방식

$$
a^n = \begin{cases}
1 & \text{if } n = 0 \\
(a^{n/2})^2 & \text{if } n \text{ is even} \\
a \times (a^{n/2})^2 & \text{if } n \text{ is odd}
\end{cases}
$$

```cpp
long long modPow(long long a, long long n, long long m) {
  long long result = 1;
  a %= m;

  while (n > 0) {
    if (n & 1) {
      result = result * a % m;
    }
    a = a * a % m;
    n >>= 1;
  }

  return result;
}
```

**시간 복잡도**: $$O(\log n)$$

<br>

### 사용 예시

```cpp
// 2^10 mod 1000 = 1024 mod 1000 = 24
cout << modPow(2, 10, 1000) << "\n";  // 24

// 3^100 mod 1000000007
cout << modPow(3, 100, 1000000007) << "\n";
```

<br>

## 모듈러 역원

<br>

$$a$$의 모듈러 역원은 $$a \times a^{-1} \equiv 1 \pmod{m}$$을 만족하는 $$a^{-1}$$입니다.

<br>

### 페르마의 소정리

$$m$$이 **소수**이고 $$\gcd(a, m) = 1$$이면:

$$a^{m-1} \equiv 1 \pmod{m}$$

따라서:

$$a^{-1} \equiv a^{m-2} \pmod{m}$$

```cpp
long long modInverse(long long a, long long m) {
  return modPow(a, m - 2, m);
}
```

<br>

### 확장 유클리드 알고리듬

$$m$$이 소수가 아닐 때 사용:

```cpp
long long extGcd(long long a, long long b, long long& x, long long& y) {
  if (b == 0) {
    x = 1;
    y = 0;
    return a;
  }

  long long x1, y1;
  long long g = extGcd(b, a % b, x1, y1);
  x = y1;
  y = x1 - (a / b) * y1;

  return g;
}

long long modInverseExt(long long a, long long m) {
  long long x, y;
  long long g = extGcd(a, m, x, y);

  if (g != 1) return -1;  // 역원 없음

  return (x % m + m) % m;
}
```

<br>

## 모듈러 나눗셈

<br>

$$\frac{a}{b} \mod m = a \times b^{-1} \mod m$$

```cpp
long long modDiv(long long a, long long b, long long m) {
  return modMul(a, modInverse(b, m), m);
}
```

**주의**: $$b$$와 $$m$$이 서로소여야 역원이 존재합니다.

<br>

## 실전 활용

<br>

### 1. 이항 계수 (nCr)

큰 수의 조합을 구할 때:

```cpp
const long long MOD = 1000000007;
const int MAXN = 100001;

long long fact[MAXN], invFact[MAXN];

void precompute() {
  fact[0] = 1;
  for (int i = 1; i < MAXN; i++) {
    fact[i] = fact[i - 1] * i % MOD;
  }

  invFact[MAXN - 1] = modPow(fact[MAXN - 1], MOD - 2, MOD);
  for (int i = MAXN - 2; i >= 0; i--) {
    invFact[i] = invFact[i + 1] * (i + 1) % MOD;
  }
}

long long nCr(int n, int r) {
  if (r < 0 || r > n) return 0;
  return fact[n] * invFact[r] % MOD * invFact[n - r] % MOD;
}
```

<br>

### 2. 피보나치 수열

```cpp
long long fib(long long n, long long m) {
  if (n <= 1) return n;

  vector<vector<long long>> M = {{1, 1}, {1, 0}};
  vector<vector<long long>> result = {{1, 0}, {0, 1}};

  auto matMul = [&](vector<vector<long long>>& A,
                    vector<vector<long long>>& B) {
    vector<vector<long long>> C(2, vector<long long>(2, 0));
    for (int i = 0; i < 2; i++) {
      for (int j = 0; j < 2; j++) {
        for (int k = 0; k < 2; k++) {
          C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % m;
        }
      }
    }
    return C;
  };

  n--;
  while (n > 0) {
    if (n & 1) result = matMul(result, M);
    M = matMul(M, M);
    n >>= 1;
  }

  return result[0][0];
}
```

<br>

### 3. 해시 계산

문자열 해싱:

```cpp
long long polyHash(const string& s, long long base, long long mod) {
  long long hash = 0;
  long long power = 1;

  for (char c : s) {
    hash = (hash + (c - 'a' + 1) * power) % mod;
    power = power * base % mod;
  }

  return hash;
}
```

<br>

## 자주 쓰는 MOD 값

<br>

| 값 | 설명 |
|---|------|
| $$10^9 + 7$$ | 가장 흔한 소수 MOD |
| $$10^9 + 9$$ | 해싱에 자주 사용 |
| $$998244353$$ | NTT에 사용 ($$2^{23} \times 7 \times 17 + 1$$) |

<br>

$$10^9 + 7$$이 자주 쓰이는 이유:
- 소수이므로 페르마 정리 적용 가능
- `int` 두 개 곱해도 `long long` 범위 내
- 외우기 쉬움

<br>

## 주의사항

<br>

**1. 오버플로우**

```cpp
// 위험: a * b가 long long 범위 초과 가능
long long result = a * b % m;

// 안전: 먼저 mod 적용
long long result = (a % m) * (b % m) % m;
```

<br>

**2. 음수 처리**

```cpp
// C++에서 음수 % 양수 = 음수 가능
int x = -7 % 5;  // -2

// 양수로 만들기
int x = ((-7 % 5) + 5) % 5;  // 3
```

<br>

**3. 역원 존재 조건**

$$\gcd(a, m) = 1$$일 때만 역원이 존재합니다.

<br>

## 마무리

모듈러 연산은 큰 수를 다루는 알고리듬 문제에서 필수적인 기법입니다.

<br>

**핵심 포인트**
- **기본 연산**: 덧셈, 뺄셈, 곱셈에 mod 분배
- **거듭제곱**: $$O(\log n)$$ 분할 정복
- **역원**: 페르마 정리 또는 확장 유클리드
- **나눗셈**: 역원을 곱하는 방식으로 계산

<br>

### 관련 글
- [유클리드 알고리듬(Euclidean Algorithm) - soo:bak](https://soo-bak.github.io/algorithm/theory/euclidean-algorithm/)
- [확장 유클리드 알고리듬(Extended Euclidean Algorithm) - soo:bak](https://soo-bak.github.io/algorithm/theory/extended-euclidean/)

<br>

### 관련 문제
- [[백준 11401] 이항 계수 3](https://www.acmicpc.net/problem/11401)
- [[백준 11444] 피보나치 수 6](https://www.acmicpc.net/problem/11444)


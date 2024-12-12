---
layout: single
title: "[백준 10816] 숫자 카드 2 (C#, C++) - soo:bak"
date: "2024-12-13 03:40:00 +0900"
description: 자료 구조, 정렬, 이분 탐색, 해시를 사용한 집합과 맵을 활용한 백준 10816번 문제를 C#과 C++로 풀이 및 해설
---

## 문제 링크
[10816번 - 숫자 카드 2](https://www.acmicpc.net/problem/10816)

## 설명
숫자 카드의 개수를 효율적으로 계산하는 문제입니다.<br>
<br>

### 문제 이해
1. 상근이가 가진 숫자 카드의 개수 `N`과 카드에 적힌 `N`개의 숫자가 주어집니다.<br>
2. 숫자 카드의 개수를 확인해야 할 숫자 `M`과 그 `M`개의 숫자가 주어집니다.<br>
3. 각 숫자에 대해, 상근이가 몇 개의 카드를 가지고 있는지 구해야 합니다.<br>
<br>

### 접근법
- **이분 탐색**을 사용하여 효율적으로 각 숫자의 개수를 구합니다.<br>
- 먼저 상근이가 가진 숫자 카드를 **정렬**합니다.<br>
- 확인할 숫자에 대해 이분 탐색으로 **좌측 경계(left bound)**와 **우측 경계(right bound)**를 찾아 개수를 계산합니다.<br>

#### 예제 시뮬레이션
입력:<br>
```
10
6 3 2 10 10 10 -10 -10 7 3
8
10 9 -5 2 3 4 5 -10
```

<br>
과정:<br>
1. 상근이가 가진 숫자 카드를 정렬하면 `[-10, -10, 2, 3, 3, 6, 7, 10, 10, 10]`이 됩니다.<br>
2. 확인할 숫자에 대해 좌측 경계와 우측 경계를 찾아 개수를 계산합니다.<br>
   - `10`의 개수: `3`<br>
   - `9`의 개수: `0`<br>
   - `-5`의 개수: `0`<br>
   - `2`의 개수: `1`<br>
   - `3`의 개수: `2`<br>
   - `4`의 개수: `0`<br>
   - `5`의 개수: `0`<br>
   - `-10`의 개수: `2`<br>

결과는 `3 0 0 1 2 0 0 2`입니다.<br>

<br>

- - -

## Code
<b>[ C# ] </b>
<br>

```csharp
namespace Solution {
  class Program {
    static void Main(string[] args) {
      int n = int.Parse(Console.ReadLine()!);
      var cards = Console.ReadLine()!
                   .Split()
                   .Select(int.Parse)
                   .OrderBy(x => x)
                   .ToArray();

      int m = int.Parse(Console.ReadLine()!);
      var nums = Console.ReadLine()!.Split().Select(int.Parse);

      var result = new List<int>();
      foreach (var num in nums) {
        int left = LowerBound(cards, num);
        int right = UpperBound(cards, num);
        result.Add(right - left);
      }

      Console.WriteLine(string.Join(" ", result));
    }

    static int LowerBound(int[] arr, int target) {
      int low = 0, high = arr.Length;
      while (low < high) {
        int mid = (low + high) / 2;
        if (arr[mid] >= target) high = mid;
        else low = mid + 1;
      }
      return low;
    }

    static int UpperBound(int[] arr, int target) {
      int low = 0, high = arr.Length;
      while (low < high) {
        int mid = (low + high) / 2;
        if (arr[mid] > target) high = mid;
        else low = mid + 1;
      }
      return low;
    }
  }
}
```
<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<int> vi;

int LowerBound(const vi& arr, int target) {
  int low = 0, high = arr.size();
  while (low < high) {
    int mid = (low + high) / 2;
    if (arr[mid] >= target) high = mid;
    else low = mid + 1;
  }
  return low;
}

int UpperBound(const vi& arr, int target) {
  int low = 0, high = arr.size();
  while (low < high) {
    int mid = (low + high) / 2;
    if (arr[mid] > target) high = mid;
    else low = mid + 1;
  }
  return low;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntCard; cin >> cntCard;

  vi cards(cntCard);
  for (int i = 0; i < cntCard; i++)
    cin >> cards[i];

  sort(cards.begin(), cards.end());

  int cntNum; cin >> cntNum;
  vi nums(cntNum);
  for (int i = 0; i < cntNum; i++)
    cin >> nums[i];

  for (const auto& num : nums) {
    int left = LowerBound(cards, num);
    int right = UpperBound(cards, num);
    cout << right - left << " ";
  }
  cout << "\n";

  return 0;
}
```

from typing import Iterator, Tuple, List
from functools import cmp_to_key


class LCPSuffixArray:
    """
    This class implements a suffix array using the LCP as described in the paper
    "Suffix arrays: A new method for on-line string searches" by Manber and
    Mayers.
    """

    def __init__(self, txt: str):
        self.__txt = txt

        # Building the array of all suffixes
        self.__pos = [i for i in range(len(self.__txt))]
        self.__sort_suffix_array()

    def __sort_suffix_array(self) -> None:
        """
        Sort the suffix array using the prefix doubling technique.
        """
        n = len(self.__txt)
        cnt = [0] * n
        prm = [0] * n
        link = [0] * n
        bh = [False] * (n + 1)
        b2h = [False] * (n + 1)

        first_char_sort = lambda x1, x2: \
            -1 if self.__txt[x1] <= self.__txt[x2] else 1

        self.__pos.sort(key=cmp_to_key(first_char_sort))

        for i in range(n):
            bh[i] = i == 0 or self.__txt[self.__pos[i]] != self.__txt[self.__pos[i - 1]]

        h = 1
        while h < n:
            i = 0

            while i < n:
                j = i + 1
                while j < n and not bh[j]:
                    j += 1
                link[i] = j
                i = j

            i = 0
            while i < n:
                cnt[i] = 0

                for j in range(i, link[i]):
                    prm[self.__pos[j]] = i

                i = link[i]

            cnt[prm[n - h]] += 1
            b2h[prm[n - h]] = True

            i = 0
            while i < n:
                for j in range(i, link[i]):
                    d = self.__pos[j] - h

                    if d >= 0:
                        c = prm[d]
                        prm[d] = c + cnt[c]
                        cnt[c] += 1
                        b2h[prm[d]] = True
                
                for j in range(i, link[i]):
                    d = self.__pos[j] - h
                    if d >= 0 and b2h[prm[d]]:
                        k = prm[d] + 1
                        while not bh[k] and b2h[k]:
                            b2h[k] = False
                            k += 1

                i = link[i]

            for i in range(n):
                self.__pos[prm[i]] = i
                if not bh[i]:
                    bh[i] = b2h[i]
            
            h *= 2
        
    def get_sorted_pos(self) -> List[int]:
        """
        Returns the suffix array.
        """
        return self.__pos

    def evaluate(self, needle: str) -> Iterator[Tuple[int, int]]:
        """
        Returns all pair of indices where a needle occur in the text.
        """
        start = self.__binary_search(needle)
        end = self.__binary_search_last_prefix_index(needle)

        while start <= end:
            yield (self.__pos[start], self.__pos[start] + len(needle))
            start += 1

    def __binary_search(self, needle: str) -> int:
        """
        Returns the smallest index such that the needle are smaller than or 
        equal all the suffixes from the suffix array starting at the index.
        """
        p = len(needle)
        n = len(self.__txt)

        l = lcp(self.__get_txt_from_sorted_index(0), needle)
        r = lcp(self.__get_txt_from_sorted_index(n - 1), needle)

        # The needle is less than the smallest suffix from the suffix array
        if l == p or needle[l] <= self.__get_txt_from_sorted_index(0)[l]:
            return 0
        # The needle is bigger than the biggest suffix from the suffix array
        elif r < p and needle[r] > self.__get_txt_from_sorted_index(n - 1)[r]:
            return n

        low = 0
        high = n - 1

        while high - low > 1:
            m = (low + high) // 2
            m_str = self.__get_txt_from_sorted_index(m)

            Llcp = lcp(self.__get_txt_from_sorted_index(low), m_str)
            Rlcp = lcp(self.__get_txt_from_sorted_index(high), m_str)

            tmp = 0

            if l >= r:
                if Llcp >= l:
                    tmp = l + lcp(m_str[l:], needle[l:])
                else:
                    tmp = Llcp
            else:
                if Rlcp >= r:
                    tmp = r + lcp(m_str[r:], needle[r:])
                else:
                    tmp = Rlcp
            
            if tmp == p or needle[tmp] <= m_str[tmp]:
                high, r = m, tmp
            else:
                low, l = m, tmp

        return high

    def __binary_search_last_prefix_index(self, needle: str) -> int:
        """
        Returns the biggest index such that the needle are bigger than or equal
        all suffixes from the suffix array with index less than or equal
        the returned index.
        """
        p = len(needle)
        n = len(self.__txt)

        l = lcp(self.__get_txt_from_sorted_index(0), needle)
        r = lcp(self.__get_txt_from_sorted_index(n - 1), needle)

        low = 0
        high = n - 1

        while high - low > 1:
            m = (low + high) // 2
            m_str = self.__get_txt_from_sorted_index(m)

            Llcp = lcp(self.__get_txt_from_sorted_index(low), m_str)
            Rlcp = lcp(self.__get_txt_from_sorted_index(high), m_str)

            tmp = 0

            if l >= r:
                if Llcp >= l:
                    tmp = l + lcp(m_str[l:], needle[l:])
                else:
                    tmp = Llcp
            else:
                if Rlcp >= r:
                    tmp = r + lcp(m_str[r:], needle[r:])
                else:
                    tmp = Rlcp
            
            if tmp == p or needle[tmp] >= m_str[tmp]:
                low, l = m, tmp
            else:
                high, r = m, tmp

        return low

    def __get_txt_from_sorted_index(self, i: int) -> str:
        return self.__txt[self.__pos[i]:]


def lcp(v: str, w: str) -> int:
    """
    Calculates the lcp (longest common prefix) between two strings v and w.
    """
    n = min(len(v), len(w))

    lcp = 0

    for i in range(n):
        if v[i] == w[i]:
            lcp += 1
        else:
            break

    return lcp
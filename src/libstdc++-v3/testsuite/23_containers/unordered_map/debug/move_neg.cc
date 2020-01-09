// Copyright (C) 2014-2015 Free Software Foundation, Inc.
//
// This file is part of the GNU ISO C++ Library.  This library is free
// software; you can redistribute it and/or modify it under the
// terms of the GNU General Public License as published by the
// Free Software Foundation; either version 3, or (at your option)
// any later version.

// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License along
// with this library; see the file COPYING3.  If not see
// <http://www.gnu.org/licenses/>.

// { dg-options "-std=gnu++11" }
// { dg-do run { xfail *-*-* } }

#include <debug/unordered_map>

#include <testsuite_hooks.h>
#include <testsuite_allocator.h>

using __gnu_test::uneq_allocator;

void test01()
{
  bool test __attribute__((unused)) = true;

  typedef uneq_allocator<std::pair<const int, int> > alloc_type;
  typedef __gnu_debug::unordered_map<
    int, int, std::hash<int>, std::equal_to<int>, alloc_type> test_type;

  test_type v1(alloc_type(1));
  v1 = { { 0, 0 } };
  auto it = v1.begin();

  test_type v2(std::move(v1), alloc_type(2));

  VERIFY( it->first == 0 );
}

int main()
{
  test01();
  return 0;
}

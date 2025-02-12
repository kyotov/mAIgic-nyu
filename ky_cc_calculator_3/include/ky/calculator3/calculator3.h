#pragma once

#include <memory>
namespace ky::calculator3 {

class Calculator3 {
public:
  Calculator3(int seed);
  ~Calculator3();

  int add(int x, int y) const;

  static int mul(int x, int y);

private:
  struct Impl;
  std::unique_ptr<Impl> pimpl_;
};

} // namespace ky::calculator3
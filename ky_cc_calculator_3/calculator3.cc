#include <ky/calculator3/calculator3.h>

namespace ky::calculator3 {

struct Calculator3::Impl {
  int seed;
};

Calculator3::Calculator3(int seed) : pimpl_(std::make_unique<Impl>(42)) {}

Calculator3::~Calculator3() = default;

int Calculator3::add(int x, int y) const { return x + y + pimpl_->seed; }

int Calculator3::mul(int x, int y) { return x * y; }

} // namespace ky::calculator3
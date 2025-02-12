#include <ky/calculator2/api.h>
#include <ky/calculator2/registrar.h>

namespace {

class Calculator2Impl : public ky::calculator2::Calculator2 {
public:
  Calculator2Impl(float seed) : seed(seed) {}

  float binary_operation(float x, float y) const override {
    return x + y + seed;
  }

private:
  float seed;
};

} // namespace

void register_calculator2seed() {
  auto &instance = ky::calculator2::registrar::get_pimpl();
  instance = std::make_unique<Calculator2Impl>(420);
}

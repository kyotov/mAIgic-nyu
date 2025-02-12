#include "ky/calculator2/registrar.h"
#include <ky/calculator2/api.h>
#include <stdexcept>

namespace ky::calculator2 {

Calculator2::~Calculator2() {}

const Calculator2 &Calculator2::get_instance() {
  auto &instance = registrar::get_pimpl();
  if (instance == nullptr) {
    throw std::runtime_error("instance not set");
  }
  return *instance;
}

} // namespace ky::calculator2

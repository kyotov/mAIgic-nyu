#include <ky/calculator2/registrar.h>

namespace ky::calculator2::registrar {

std::unique_ptr<Calculator2> &get_pimpl() {
  static std::unique_ptr<Calculator2> storage;
  return storage;
}

} // namespace ky::calculator2::registrar

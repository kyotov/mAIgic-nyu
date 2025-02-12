#pragma once

#include <ky/calculator2/api.h>
#include <memory>

namespace ky::calculator2::registrar {

std::unique_ptr<Calculator2> &get_pimpl();

}
# Maintainer: kartavkun <nikitarobezhko@yandex.ru>
pkgname=osufetch-bin
pkgver=1.1.0
pkgrel=1
pkgdesc="Minimal terminal osu! profile viewer"
arch=('x86_64')
url="https://github.com/kartavkun/osufetch"
license=('MIT')
depends=('glibc')
provides=('osufetch')
conflicts=('osufetch')
source=("osufetch::${url}/releases/download/v${pkgver}/osufetch")
sha256sums=('49fe4dbda948954efd676f3461b8248e4c06d5d5da9df87e95861edb123075ee')

package() {
  install -Dm755 "$srcdir/osufetch" "$pkgdir/usr/bin/osufetch"
}

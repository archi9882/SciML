! 舊版河道洪水演算求解器（Fortran 90）：1D 對流擴散，upwind + 中央差分，顯式時間積分。
! 編譯：gfortran -O2 legacy/transport.f90 -o transport
program transport
  implicit none
  integer, parameter :: n = 100, nsteps = 400
  real(8), parameter :: l = 10.0d0, d = 0.5d0, u = 0.68d0, dt = 0.0096d0
  real(8) :: dx, x, c(n), cn(n)
  integer :: i, step

  dx = l / n

  ! 初始條件：靠近下游出口的高斯形洪峰
  do i = 1, n
    x = (i - 0.5d0) * dx
    c(i) = exp(-((x - 8.0d0) / 0.5d0)**2)
  end do

  do step = 1, nsteps
    cn(1) = 0.0d0                        ! 上游端：擾動固定為 0
    do i = 2, n - 1
      cn(i) = c(i) - u * dt * (c(i) - c(i-1)) / dx &
              + d * dt * (c(i+1) - 2.0d0 * c(i) + c(i-1)) / dx**2
    end do
    cn(n) = cn(n-1)                      ! 下游端：零梯度（自由流出）
    c = cn
  end do

  write(*, '(A,F10.6)') 'peak = ', maxval(c)
  write(*, '(A,F10.6)') 'sum  = ', sum(c)
end program transport

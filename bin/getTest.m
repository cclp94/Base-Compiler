          %== CODE FOR: ./bin/getTest.m ==%
f1        sw 0(R14), R15
          lw R11, 12(R14)
          lw R10, 8(R14)
          add R12, R10, R11
          sw 16(R14), R12
          lw R12, 16(R14)
          sw 4(R14), R12
          lw R15, 0(R14)
          jr R15
          entry  % program entry
          align
          addi R14, R0, topaddr  % init stack pointer register
          addi R15, R0, topaddr  % init frame pointer register
          subi R14, R14, 12  % Set stack to top
          jl R15, getint
          sw 0(R14), R1
          getc R1
          jl R15, getint
          sw 4(R14), R1
          getc R1
          lw R10, 4(R14)
          lw R11, 0(R14)
          add R12, R11, R10
          sw 8(R14), R12
          lw R1, 8(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          hlt  % program exit
          %== END OF PROGRAM ==%
buf       res 20  % mem for moon lib subroutines

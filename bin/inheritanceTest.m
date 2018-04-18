          %== CODE FOR: ./bin/inheritanceTest.m ==%
f1        sw 0(R14), R15
          addi R1, R0, 100
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
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
          lw R1, 4(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          lw R1, 0(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          addi R14, R14, -8
          jl R15, f1
          addi R14, R14, 8
          lw R12, -4(R14)
          sw 8(R14), R12
          lw R1, 8(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          hlt  % program exit
          %== END OF PROGRAM ==%
buf       res 20  % mem for moon lib subroutines

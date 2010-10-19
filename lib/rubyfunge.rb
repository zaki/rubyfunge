class RubyFunge
  attr_reader :x
  attr_reader :y
  attr_reader :stack
  attr_reader :code

  DIRS = [:left, :right, :up, :down]

  def initialize()
    @x, @y    = 0, 0
    @dir      = :right
    @code     = []
    @stack    = []
    @str_mode = false
    @skip     = false

    @synt   = {
                '+'=>:op_add, '-'=>:op_sub, '*'=>:op_mul, '/'=>:op_div, '%'=>:op_mod,
                '!'=>:op_not, '`'=>:op_gt,
                '>'=>:op_right, '<'=>:op_left, '^'=>:op_up, 'v'=>:op_down,
                '?'=>:op_rnd,
                '_'=>:op_lr, '|'=>:op_ud,
                '"'=>:op_str,
                ':'=>:op_dup, '\\'=>:op_swp,
                '$'=>:op_pop, '.'=>:op_outi, ','=>:op_outc,
                '#'=>:op_skp, 'p'=>:op_put, 'g'=>:op_get,
                '&'=>:op_aski, '~'=>:op_askc
              }
  end

  def run(code)
    i = 0
    @code = []
    code.each_line {|l|
      @code[i] = l
      i += 1
    }
    @x, @y = 0,0
    while (@code[@y][@x].chr != '@')
      op = @code[@y][@x].chr
      if (@str_mode)
        if (op == '"')
          op_str
        else
          push op[0]
        end
      elsif (op=='#')
        @skip = true
      elsif (op=~/\d/ && !@skip)
        self.send :push, op.to_i
        @skip = false
      else
        self.send @synt[op] if @synt.include?(op) && !@skip
        @skip = false
      end
      case @dir
        when :right
          @x += 1
          @x = 0 if @x > @code[@y].length - 1
        when :left
          @x -= 1
          @x = @code[@y].length - 1 if @x < 0
        when :up
          @y -= 1
          @y = @code.length - 1 if @y < 0
        when :down
          @y += 1
          @y = 0 if @y > @code.length - 1
      end
    end
  end

  # Instructions
  def push(num)
    @stack.push num
  end

  def op_right
    @dir = :right
  end

  def op_down
    @dir = :down
  end

  def op_up
    @dir = :up
  end

  def op_left
    @dir = :left
  end

  def op_pop
    pop
  end

  def op_add
    push pop+pop
  end

  def op_sub
    push -pop+pop
  end

  def op_mul
    push pop*pop
  end

  def op_div
    a,b=pop,pop
    if a == 0
      push $stdin.readline.to_i
    else
      push b/a
    end
  end

  def op_mod
    a,b=pop,pop
    if a == 0
      push $stdin.readline.to_i
    else
      push b%a
    end
  end

  def op_not
    push pop == 0 ? 1 : 0
  end

  def op_gt
    push pop <= pop ? 0 : 1
  end

  def op_rnd
    @dir = DIRS[rand DIRS.length]
  end

  def op_lr
    @dir = pop == 0 ? :right : :left
  end

  def op_ud
    @dir = pop == 0 ? :down : :up
  end

  def op_str
    @str_mode = !@str_mode
  end

  def op_dup
    a = pop
    push a; push a
  end

  def op_swp
    a,b = pop, pop
    push a; push b
  end

  def op_outi
    print pop
  end

  def op_outc
    print pop.chr
  end

  def op_get
    y,x = pop, pop
    push @code[x][y]
  end

  def op_put
    v,y,x = pop, pop,pop
    @code[x][y] = v.chr
  end

  def op_aski
    c = $stdin.readline
    push c.to_i
  end

  def op_askc
    c = $stdin.getc
    push c
  end

private
  def pop
    return 0 if @stack.length == 0
    @stack.pop
  end
end

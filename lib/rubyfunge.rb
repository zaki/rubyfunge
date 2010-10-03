class RubyFunge
  attr_reader :x
  attr_reader :y
  attr_reader :stack
  attr_reader :code

  def initialize()
    @x, @y  = 0, 0
    @dir    = :right
	@code   = []
	@stack  = []

    @synt   = {
                '+'=>:op_add, '-'=>:op_sub, '*'=>:op_mul, '/'=>:op_div, '%'=>:op_mod,
                '!'=>:op_not, '`'=>:op_gt,
                '>'=>:op_right, '<'=>:op_left, '^'=>:op_up, 'v'=>:op_down,
                '?'=>:op_rnd,
                '_'=>:op_lr, '|'=>:op_ud,
                '"'=>:op_str,
                ':'=>:op_dup, '\\'=>:op_swap,
                '$'=>:op_pop, '.'=>:op_outi, ','=>:op_outc,
                '#'=>:op_skp, 'P'=>:op_put, 'g'=>:op_get,
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
      self.send @synt[op] if @synt.include? op
      case @dir
        when :right
          @x += 1
        when :left
          @x -= 1
        when :up
          @y -= 1
        when :down
          @y += 1
      end
    end
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
end

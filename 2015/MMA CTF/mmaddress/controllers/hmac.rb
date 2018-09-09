module HMAC
  def xor_str(x, y)
    x.unpack("C*").zip(y.unpack("C*")).map{|x, y| (x ^ y)}.pack("C*")
  end

  def ipad(len)
    "\x36" * len
  end

  def opad(len)
    "\x5c" * len
  end

  def hmac(message, key, bits)
    raise ArgumentError.new("No block given.") unless block_given?
    raise ArgumentError.new("Too long key.") unless key.size <= bits / 8
    key += "\0" while key.size < bits / 8
    yield(xor_str(key, opad(bits / 8)) + yield(xor_str(key, ipad(bits / 8)) + message))
  end

  module_function :hmac, :opad, :ipad, :xor_str
end

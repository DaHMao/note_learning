import redis


class RedisClientClass:
    def __init__(self):
        pool = redis.ConnectionPool(host='192.168.1.101', port=6379, decode_responses=True, db=1,
                                    password='')
        self.r = redis.Redis(connection_pool=pool)

    # -------------------------------------------------列表--------------------------------------------------
    def add_value_push(self, name, value):
        """
        向redis指定库添加 lpush
        :param name:  表名
        :param value: 字符串数据
        :return:
        """
        # r.lpush(name,value) 向列表的表头插入一个或者多个值
        # r.rpush(name,value) 向列表的表尾插入一个或者多个值
        self.r.lpush(name, value)

    def out_value_push(self, name, end, start=0):
        """
        返回指定区间的元素
        :param name:
        :param start:
        :param end:
        :return: 列表
        """
        return self.r.lrange(name, start, end)

    def key_pop(self, key):
        """
        移除并返回 列表 key 的元素
        :param key:
        :return:
        """
        # r.rpop(key) 移除列表的尾部元素
        # r.lpop(key) 移除列表的头部元素
        # r.blpop(key,timeout) 移出并获取列表的第一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止
        # r.blpop(key,timeout) 移出并获取列表的最后一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止
        return self.r.rpop(key)

    def key_index(self, name, index):
        """
        通过索引获取列表的元素
        :param name:
        :param index:  索引，可以为负数
        :return:
        """
        return self.r.lindex(name, index)

    def key_len(self, name):
        """
        返回列表的长度
        :param name:
        :return:
        """
        return self.r.llen(name)

    def key_brpoplpush(self, source, destination, timeout=2):
        """
        命令从列表中弹出一个值，将弹出的元素插入到另外一个列表中并返回它；
        如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止
        :param source: 原来的列表
        :param destination: 添加元素的列表
        :param timeout: 超时
        :return:
        """
        return self.r.brpoplpush(source, destination, timeout=timeout)

    def key_insert(self, key, privot, value, where="AFTER"):
        """
        用于在列表的元素前或者后插入元素
        :param key: 表名
        :param where: "BEFORE" or "AFTER"
        :param privot: 列表元素的值
        :param value:
        :return: 列表的长度
        """
        return self.r.linsert(name=key, where=where, refvalue=privot, value=value)

    # r.lpushx(key)
    #   将一个或多个值插入到已存在的列表头部，列表不存在时操作无效
    #       注：lpush的区别是lpushx在列表不存在时操作无效，而lpush会创建一个列表
    # r.lrem(key, value, count)
    #    根据参数 COUNT 的值，移除列表中与参数 VALUE 相等的元素。
    #       COUNT 的值可以是以下几种：
    #         count > 0 : 从表头开始向表尾搜索，移除与 VALUE 相等的元素，数量为 COUNT 。
    #         count < 0 : 从表尾开始向表头搜索，移除与 VALUE 相等的元素，数量为 COUNT 的绝对值。
    #         count = 0 : 移除表中所有与 VALUE 相等的值。
    # 返回被移除元素的数量。 列表不存在时返回 0 。
    # lset(key , index , value)
    #   将列表 key 下标为 index 的元素的值设置为 value 。
    #       当 index 参数超出范围，或对一个空列表( key 不存在)进行 LSET 时，返回一个错误。
    # ltrim(key , start , stop)
    #   对一个列表进行修剪(trim)，就是说，让列表只保留指定区间内的元素，不在指定区间之内的元素都将被删除。
    #       举个例子，执行命令 LTRIM list 0 2 ，表示只保留列表 list 的前三个元素，其余元素全部删除。
    #       下标(index)参数 start 和 stop 都以 0 为底，也就是说，以 0 表示列表的第一个元素，以 1 表示列表的第二个元素，以此类推。
    #       你也可以使用负数下标，以 -1 表示列表的最后一个元素， -2 表示列表的倒数第二个元素，以此类推。
    # rpoplpush(source , destination)
    #   将列表 source 中的最后一个元素(尾元素)弹出，并返回给客户端。
    #       将 source 弹出的元素插入到列表 destination ，作为 destination 列表的的头元素。
    # rpushx(key , value)
    #   将值 value 插入到列表 key 的表尾，当且仅当 key 存在并且是一个列表。
    #       和 RPUSH 命令相反，当 key 不存在时， RPUSHX 命令什么也不做。

    # -------------------------------------------------字符串--------------------------------------------------
    # r.set(key,value)
    #   SET 命令用于设置给定 key 的值。如果 key 已经存储其他值， SET 就覆写旧值，且无视类型
    #     插入成功后返回True
    # r.getset(key,value)
    #   命令用于设置指定 key 的值，
    #       并返回 key 旧的值，
    #       当 key 存在但不是字符串类型时，返回一个错误。
    # r.get(key)
    #   Get 命令用于获取指定 key 的值。
    #       如果 key 不存在，返回 None 。
    #       如果key 储存的值不是字符串类型，返回一个错误。
    def get_range(self, key, start=0, end=5):
        """
        Getrange 命令用于获取存储在指定 key 中字符串的子字符串。字符串的截取范围由 start 和 end 两个偏移量决定(包括 start 和 end 在内)。
        :param key:
        :param start:
        :param end:
        :return: 截取的字符串
        """
        self.r.set(key, "Hello world!")
        return self.r.getrange(key=key, start=start, end=end)

    def get_bit(self, key, offset):
        """
         命令用于对 key 所储存的字符串值，获取指定偏移量上的位(bit)字符串值指定偏移量上的位(bit)
        :param key:
        :param offset:
        :return: 当偏移量 getrange 比字符串值的长度大，或者 key 不存在时，返回 0
        """
        return self.r.getbit(key, offset=offset)

    def get_m(self):
        """
        命令返回所有(一个或多个)给定 key 的值。 如果给定的 key 里面，有某个 key 不存在，那么这个 key 返回特殊值 None
        :return: list ['Holle world!', None]
        """
        return self.r.mget("list", "list2")

    def set_ex(self, key, value, timeout):
        """
        命令为指定的 key 设置值及其过期时间
        :param key:
        :param value:
        :param timeout: 过期时长
        :return:
        """
        # r.psetex(name, time, value)  以毫秒为单位设置 name 的生存时间
        # r.setex(name, time, value)   以秒为单位设置 name 的生存时间
        return self.r.setex(name=key, time=timeout, value=value)

    # r.setnx（name,value）
    #     命令在指定的 name 不存在时，为 name 设置指定的值。设置成功，返回 1 。 设置失败，返回 0 。
    # r.setrange(name, offset, value)
    #     命令用指定的字符串覆盖给定 name 所储存的字符串值，覆盖的位置从偏移量 offset 开始, 返回设置后的字符串的长度
    # r.strlen(name)
    #     命令用于获取指定 name 所储存的字符串值的长度。当 name 储存的不是字符串值时，返回一个错误。
    # r.mset(name1="1", name2='2')
    #     命令用于同时设置一个或多个 key-value
    # r.msetnx(name5="5", name6='6')
    #     命令用于所有给定 key 都不存在时，同时设置一个或多个 key-value 。
    #     当所有 key 都成功设置，返回 1 。 如果所有给定 key 都设置失败(至少有一个 key 已经存在)，那么返回 0 。

    # r.incr(name)
    #    命令将 name 中储存的数字值增一
    #       如果 name 不存在，那么 name 的值会先被初始化为 0 ，然后再执行 incr 操作;
    #       如果值包含错误的类型，或字符串类型的值不能表示为数字，那么返回一个错误
    # r.incrby(name,value)
    # r.incrbyfloat(name,value)
    #   命令将 name 中储存的数字加上指定的value
    #       如果 name 不存在，那么 name 的值会先被初始化为 0 ，然后再执行 INCRBY 命令。
    #       如果值包含错误的类型，或字符串类型的值不能表示为数字，那么返回一个错误
    # r.decr(name，amount=1)
    #     命令将 name 中储存的数字值减一，amount 表示减的数值

    # r.append(name, value)
    #     命令用于为指定的 key 追加值,返回字符串的长度
    #       如果 key 已经存在并且是一个字符串， APPEND 命令将 value 追加到 key 原来的值的末尾。
    #       如果 key 不存在， APPEND 就简单地将给定 key 设为 value ，就像执行 SET key value 一样

    # -------------------------------------------------哈希(hash)--------------------------------------------------
    # r.hset(name,key,value)
    #   命令用于为哈希表中的字段赋值；
    #         如果哈希表不存在，一个新的哈希表被创建并进行 HSET 操作。
    #          如果字段已经存在于哈希表中，旧值将被覆盖。
    #          如果字段是哈希表中的一个新建字段，并且值设置成功，返回 1 。
    #          如果哈希表中域字段已经存在且旧值已被新值覆盖，返回 0 。
    # r.hget(name,key)
    #   命令用于返回哈希表中指定字段的值。返回给定字段的值。如果给定的字段或 key 不存在时，返回 None 。
    # r.delete(name)
    #   命令用于删除哈希表 name 中的一个或多个指定字段，不存在的字段将被忽略。
    # r.hexists(name,key)
    #   命令用于查看哈希表的指定字段是否存在
    #       如果哈希表含有给定字段，返回 True 。
    #       如果哈希表不含有给定字段，或 key 不存在，返回False
    # r.hgetall(name)
    #    命令用于返回哈希表中，所有的字段和值
    #       在返回值里，紧跟每个字段名(field name)之后是字段的值(value)，所以返回值的长度是哈希表大小的两倍
    # r.hincrby(name,key,amount=2)     哈希表中的字段值加上指定增量值
    # r.hincrbyfloat(name,key,amount="1.2")  哈希表中的字段值加上指定浮点数增量值
    #   增量也可以为负数，相当于对指定字段进行减法操作。
    #       如果哈希表的 key 不存在，一个新的哈希表被创建并执行 hincrby 命令。
    #       如果指定的字段不存在，那么在执行命令前，字段的值被初始化为 0 。
    #       对一个储存字符串值的字段执行 hincrby 命令将造成一个错误。

    # r.hkeys(name)
    #   hkeys命令用于获取哈希表中的所有字段名。
    #       包含哈希表中所有字段的列表。 当 key 不存在时，返回一个空列表。
    # r.hlen(name)
    #   命令用于获取哈希表中字段的数量。哈希表中字段的数量。 当 key 不存在时，返回 0 。

    # r.hmget(name,keys)
    #   用于返回哈希表中，一个或多个给定字段的值。如果指定的字段不存在于哈希表，那么返回一个 nil 值。
    #        一个包含多个给定字段关联值的表，表值的排列顺序和指定字段的请求顺序一样。

    # aa = {"a":"a","b":"b"}
    # r.hmset("name",aa)
    #   命令用于同时将多个 field-value (字段-值)对设置到哈希表中。
    #       此命令会覆盖哈希表中已存在的字段。
    #       如果哈希表不存在，会创建一个空哈希表，并执行 hmset 操作。

    # r.hsetnx(name,key,value)
    #   用于为哈希表中不存在的的字段赋值
    #       如果哈希表不存在，一个新的哈希表被创建并进行 HSET 操作。
    #       如果字段已经存在于哈希表中，操作无效。
    #       如果 key 不存在，一个新哈希表被创建并执行 HSETNX 命令。
    #       设置成功，返回 1 。 如果给定字段已经存在且没有操作被执行，返回 0

    # r.hvals(name)
    #   命令返回哈希表所有字段的值
    #       一个包含哈希表中所有值的表。 当 key 不存在时，返回一个空表。

    # -------------------------------------------------集合(set)--------------------------------------------------
    # r.sadd(name,*values)
    def set_add(self):
        """
        命令将一个或多个成员元素加入到集合中，已经存在于集合的成员元素将被忽略
        :return: 0表示元素已经存在，1表示添加元素成功
        """
        return self.r.sadd("list3", 6, 5, 7)

    # r.scard(name) 返回集合中元素的数量, 当集合 key 不存在时，返回 0,类型错误返回一个错误

    # r.sdiff(name1, name2)  命令返回集合与给定集合之间的差集。不存在的集合 key 将视为空集。
    def set_sdiff(self):
        """
        命令返回给定集合之间的差集,不存在的集合 key 将视为空集
        :return:
        """
        return self.r.sdiff("list4", "list3")

    # r.sdiffstore(name1,name2,name3) 命令将给定集合之间的差集存储在指定的集合(name3)中。如果指定的集合(name3)已存在，则会被覆盖。

    # r.sinter(name1, name2) 命令返回给定所有给定集合的交集。 不存在的集合 name 被视为空集。
    #                           当给定集合当中有一个空集时，结果也为空集(根据集合运算定律)。

    # r.sinterstore(name1,name2,name3)  命令将给定集合之间的交集存储在指定的集合(name3)中。如果指定的集合(name3)已经存在，则将其覆盖。

    #  r.sunion(name1,name2)  命令返回给定集合的并集。不存在的集合 key 被视为空集。

    # r.sunionstore((name1,name2,name3)  命令将给定集合的并集存储在指定的集合 name3 中

    # r.smembers(name)  命令返回集合中的所有的成员。 不存在的集合 key 被视为空集合。

    # r.smove(name1, name2, value)  命令将指定成员 value 元素从 name1 集合移动到 name2 集合。
    #         如果 name1 集合不存在或不包含指定的 value 元素，则 SMOVE 命令不执行任何操作，仅返回 False 。
    #                               否则，value 元素从 name1 集合中被移除，并添加到 name2 集合中去。
    #         当 name2 集合已经包含 value 元素时， SMOVE 命令只是简单地将 name1 集合中的 value 元素删除。
    #         当 name1 或 name2 不是集合类型时，返回一个错误。
    #         如果成员元素被成功移除，返回 True。
    #         如果成员元素不是 name1 集合的成员，并且没有任何操作对 name2 集合执行，那么返回 False

    # r.spop(name)  用于移除并返回集合中的一个随机元素。

    # r.srandmember(name,count) 用于返回集合中的一个随机元素
    #       如果 count 为正数，且小于集合基数，那么命令返回一个包含 count 个元素的数组，数组中的元素各不相同。
    #       如果 count 大于等于集合基数，那么返回整个集合。
    #       如果 count 为负数，那么命令返回一个数组，数组中的元素可能会重复出现多次，而数组的长度为 count 的绝对值。

    # r.srem(name, value) 用于移除集合中的一个或多个成员元素 不存在的成员元素(value)会被忽略

    def set_sscan(self):
        """
        命令用于迭代集合键中的元素
        :return:
        """
        print(self.r.sadd("list4", "hello", 2, "hi", 4, 5, 6, "hil", 8, 4))
        print(self.r.sscan(name="list4", cursor=0, match=44, count=10))
        # cursor 游标
        # match 匹配的模式
        # count 指定从数据集里返回多少元素，默认值为 10


if __name__ == "__main__":
    r = RedisClientClass()
    r.set_add()
    print(r.set_sscan())

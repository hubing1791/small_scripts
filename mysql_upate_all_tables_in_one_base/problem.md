今天在项目开发中，发现了一个小问题，使得需要修改某个数据库下所有表的某个字段。

虽然实际上手动修改也很快，但是决定学习并实现一下利用一个过程在mysql下实现。

**查询某个数据库表下的所有的表名**

首先肯定需要一个子查询，获得全部的表名，之后作为游标使用。格式如下。information_schema.tables存储了mysql种的全部表信息，我们只需要查询表名即可,DB_name是数据库名

``` sql
select table_name from information_schema.tables where table_schema= DB_name ;
```

**使用conact连接生成sql语句**

tables_cur是游标里取出来的表名

```sql 
set XXX = conact("update",tables_cur,"set xxx = xxx");
```

**将游标结束和标志位绑定的方法**

在从游标中取数的时候，怎么判断游标是否取完呢？

上网搜索查到了利用如下的语句,意为在游标遍历完的时候把xxx设为TRUE，这样就可以作为循环的跳出条件，**特别注意，下面的语句是对整个储存过程生效的**，写语句时要注意，不能在需要用到标志位之前就写了空查询，可能会导致标志位提前被修改

```sql
DECLARE CONTINUE HANDLER FOR NOT FOUND SET XXX = TRUE;
```

**使用loop循环实现**

完整的如下，这是模板，一些地方我替换成了无用信息，修改后即可使用。注意mysql中需要先生成存储过程再调用

``` sql 
CREATE DEFINER=`root`@`%` PROCEDURE `update_all`()
BEGIN
	DECLARE a VARCHAR(20);	-- 定义接收游标数据的变量 
  DECLARE SQL_CONACT varchar(100); -- 定义拼接后的sql语句 
 
  DECLARE done TINYINT DEFAULT FALSE; -- 遍历数据结束标志
  DECLARE cur CURSOR FOR (select table_name from information_schema.`TABLES` where TABLE_SCHEMA = 'XXX');  -- 游标
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;  -- 将结束标志绑定到游标
 
 -- 打开游标
  OPEN cur; 
		-- 开始循环（loop循环）
		update_loop: LOOP
			-- 提取游标里的数据
			FETCH cur INTO a;
			
			-- 声明结束的时候
			IF done THEN
				LEAVE update_loop;
			END IF;
 	
			set SQL_CONACT = concat(略); -- 拼接
			set @sql = SQL_CONACT;  
			prepare stmt from @sql; 	-- 预处理
				execute stmt;  		-- 执行
			deallocate prepare stmt;	-- 释放prepare
 
		END LOOP;
 
  -- 关闭游标
  CLOSE cur;

END
```

**需要注意**

在连接子句的表名的时候，记得加上``符号，为的是避免特殊的表名使得拼接出的sql语句出错。

**参考**

[同时修改某一个数据库中所有表的所有字段的编码格式](https://blog.csdn.net/LUNG108/article/details/78285054)

[MYSQL游标（CURSOR）关于NOT FOUND或02000结束状态只遍历一次的问题](https://blog.csdn.net/u011214505/article/details/53335944)
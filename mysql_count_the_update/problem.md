今天需要统计数据库的修改情况，就是统计已经修改数量/总数。每个数据表都有一个标志位用于修改，直接写个sql查某个表的修改是很容易的。但是为节省之后的精力，最后研究后最终实现为将统计结果写入数据库存储。

这样以后需要查就可以直接调用过程解决。

**查询数据数量**

这个十分简单，利用count()解决

``` sql
SELECT COUNT(DISTINCT id)  as `marked` FROM subrel_1 WHERE judge_submit = 1 ;
```

**使用select将结果放在一行**

为了让结果看起来比较舒服，自然是希望能在同一行中显示结果，可以用下面这种方法达到print的效果。

```sql 
set marked =  (SELECT COUNT(DISTINCT id)  as `marked` FROM xxx WHERE judge_submit = 1 );
	set all_number = (SELECT COUNT(DISTINCT id)  as `all` FROM xxx);
	SELECT marked,all_number;
```

这样显示的结果就会看着比较舒服，如下图

![截图]({{site.url}}/assets/img/2020_04_25/1.png)

**获取动态语句里的但单一查询结果的方法**

这个本该很简单，但是学艺不精，查了好一会才解决。

即动态语句中先赋值给变量，执行后在赋值一次

```sql
set SQL_CONACT = concat("SELECT COUNT(DISTINCT id) FROM`", a, "`WHERE judge_submit = 1 into @marked");
			set @sql = SQL_CONACT;  
			prepare stmt from @sql; 	-- 预处理
				execute stmt;  		-- 执行
			deallocate prepare stmt;
			SET marked = @marked;
```



**最终的实现**

完整的如下：

``` sql 
CREATE DEFINER=`root`@`%` PROCEDURE `count_marked`()
BEGIN
	#Routine body goes here...
	DECLARE a VARCHAR(50);	-- 定义接收游标数据的变量 
  DECLARE SQL_CONACT varchar(200); -- 定义拼接后的sql语句 
	
	DECLARE `marked` int; -- 已经修改的数据量
	DECLARE `all_number` int; -- 总数据量
 
  DECLARE done INT DEFAULT FALSE; -- 遍历数据结束标志
  DECLARE cur CURSOR FOR (select table_name from information_schema.`TABLES` where TABLE_SCHEMA = 'graph');  -- 游标
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;  -- 将结束标志绑定到游标
	
	 OPEN cur; 
		-- 开始循环（loop循环）
		update_loop: LOOP
			-- 提取游标里的数据
			FETCH cur INTO a;
			
			-- 声明结束的时候
			IF done THEN
				LEAVE update_loop;
			END IF;
			set SQL_CONACT = concat("SELECT COUNT(DISTINCT id) FROM`", a, "`WHERE judge_submit = 1 into @marked");
			set @sql = SQL_CONACT;  
			prepare stmt from @sql; 	
				execute stmt;  		
			deallocate prepare stmt;
			SET marked = @marked;
			
			set SQL_CONACT = concat("SELECT COUNT(DISTINCT id) FROM`", a, "`into @all_number");
			set @sql = SQL_CONACT;  
			prepare stmt from @sql; 	
				execute stmt;  		
			deallocate prepare stmt;
			set all_number = @all_number;
			-- SELECT marked,all_number,a as `table_name`; -- 显示结果
			
			set @table_name = a;
			set SQL_CONACT = "INSERT INTO progress_count.workcount (table_name,all_number,marked) VALUES(?,?,?)";
			set @sql = SQL_CONACT;  
			prepare stmt from @sql; 	
				execute stmt USING @table_name,@all_number,@marked; 
			deallocate prepare stmt;
			
			END LOOP;
 
  CLOSE cur;
END
```

**需要注意**

除了直接用变量拼接，使用？然后用execute using来传参会更简洁，用法参见最后那段

using 一开始直接@a无法获取表明，新建变量table_name再@就行
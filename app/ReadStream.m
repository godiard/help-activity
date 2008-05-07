#import "ReadStream.h"

@implementation ReadStream

-(ReadStream *) initWithString: (NSString *) s {
  [self init];
  str = s;
  pos = 0;
  return self;
}

-(unichar) safeCharAtIndex: (int) i {
  return [self isAtEnd] ? 0 : [str characterAtIndex: i];
}

-(unichar) peekBack {
  return [self safeCharAtIndex: pos - 1];
}

-(unichar) peek {
  return [self safeCharAtIndex: pos];
}

-(unichar) peekTwo {
  return [self safeCharAtIndex: pos + 1];
}

-(unichar) read {
  unichar c = [self safeCharAtIndex: pos];
  pos++;
  return c;
}

-(BOOL) isAtEnd {
  return pos == [str length];
}

-(unichar) expect: (unichar) c {
  unichar r;
  if((r = [self read]) != c) NSLog(@"WARNING: expected %c at position %d, found %c", c, pos - 1, r);
  return r;
}

-(NSString *) readUpto: (unichar) c {
  int found = pos;
  
  while(found != [str length] && [self safeCharAtIndex: found++] != c);
  //if(found == [str length]) return NULL; // not found
  
  found--;
  NSString *s = [str substringWithRange: NSMakeRange(pos, found - pos)];
  pos = found;
  
  return s;
}

/*-(NSString *) readUptoString: (NSString *) s {
  NSRange range = [str rangeOfString: s options: 0 range: NSMakeRange(pos, [str length] - pos)];
  NSString *text;

  if(range.location != NSNotFound) {
    text = [str substringToIndex: range.location];
    pos = range.location;
  } else {
    text = [str substringFromIndex: pos];
  }

  return text;
}*/

@end

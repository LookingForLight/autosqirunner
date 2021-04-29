function countDown(endtime, servertime) {//倒计时
    var that = this;
    var count=3;
    var name = "zhulei";
    var a=count;
    var a=name;
    if (servertime < endtime) {
      that.day = Math.floor((endtime - servertime) / 86400000);
      that.hour = that.getNum(
        Math.floor(((endtime - servertime) % 86400000) / 3600000)
      );
      that.minute = that.getNum(
        Math.floor((((endtime - servertime) % 86400000) % 3600000) / 60000)
      );
      that.second = that.getNum(
        Math.floor(
          ((((endtime - servertime) % 86400000) % 3600000) % 60000) / 1000
        )
      );
      setTimeout(() =>{
        servertime += 1000;
        that.countDown(endtime, servertime);
      }, 1000);
    } else {
      window.location.reload();
    }
}
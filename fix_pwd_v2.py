import re

html = open('index.html', 'r', encoding='utf-8').read()

# 1. 替换 finRenderSettings 中的安全设置部分（从"安全设置"到"数据管理"之前）
old_security = r"""  h+='<div class="fin-card"><div class="fin-card-title">🔐 安全设置</div>';
  h+='<button class="fin-save-btn" onclick="finChangePassword()" style="margin-top:0;margin-bottom:8px">🔑 修改密码</button>';
  h+='<div style="font-size:12px;color:var(--sub);line-height:1.6;padding:4px 0">当前设备ID：'+_finDeviceId().substring(0,12)+'...<br>数据已加密存储，换设备需验证密码</div></div>';"""

new_security = r"""  h+='<div class="fin-card"><div class="fin-card-title">🔐 访问密码</div>';
  var hasPwd=localStorage.getItem('fin_pwd')?'已设置':'未设置';
  h+='<div style="font-size:12px;color:var(--sub);margin-bottom:8px">当前状态：'+hasPwd+'</div>';
  h+='<button class="fin-save-btn" onclick="finShowSetPwdModal()" style="margin-top:0;margin-bottom:8px">🔑 '+(hasPwd==='已设置'?'修改密码':'设置密码')+'</button>';
  h+='<button class="fin-save-btn" onclick="finClearPwd()" style="margin-top:0;background:linear-gradient(135deg,#e17055,#d63031)">🗑️ 清除密码</button>';
  h+='<div style="font-size:11px;color:var(--sub);line-height:1.6;padding:4px 0">设置密码后，每次打开需验证<br>忘记密码会丢失所有财务数据</div></div>';"""

if old_security in html:
    html = html.replace(old_security, new_security)
    print('[OK] 替换安全设置部分')
else:
    print('[X] 未找到安全设置部分，尝试模糊匹配...')
    # 尝试去掉多余空格
    pattern = re.escape("""  h+='<div class="fin-card"><div class="fin-card-title">🔐 安全设置</div>';""")
    print('  附近代码：', html[html.find('安全设置')-50:html.find('安全设置')+200] if '安全设置' in html else '未找到')

# 2. 检查并添加 finShowSetPwdModal 和 finClearPwd 函数（如果不存在）
if 'function finShowSetPwdModal' not in html:
    # 在 </script> 前插入新函数
    new_funcs = r"""
function finShowSetPwdModal(){
  var hasPwd=!!localStorage.getItem('fin_pwd');
  var mask=document.createElement('div');mask.className='modal-mask';mask.style.zIndex='2000';
  var title=hasPwd?'🔑 修改密码':'🔑 设置密码';
  var btnText=hasPwd?'确认修改':'确认设置';
  mask.innerHTML='<div onclick="event.stopPropagation()" style="background:var(--card);border-radius:16px;padding:24px;width:300px;max-width:85vw;text-align:center;box-shadow:0 8px 30px rgba(0,0,0,.2)">'
    +'<div style="font-size:32px;margin-bottom:8px">🔐</div>'
    +'<h3 style="margin:0 0 4px;font-size:17px">'+title+'</h3>'
    +(hasPwd?'<input class="form-input" type="password" id="finOldPwd" placeholder="旧密码" style="width:100%;margin-bottom:8px;text-align:center;font-size:15px">':'')
    +'<input class="form-input" type="password" id="finNewPwd" placeholder="新密码（至少4位）" style="width:100%;margin-bottom:8px;text-align:center;font-size:15px">'
    +'<input class="form-input" type="password" id="finNewPwd2" placeholder="确认新密码" style="width:100%;margin-bottom:12px;text-align:center;font-size:15px">'
    +'<button onclick="finDoSetPwd()" style="width:100%;padding:12px;border:none;border-radius:10px;background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;font-size:15px;font-weight:700;cursor:pointer">'+btnText+'</button>'
    +'</div>';
  mask.onclick=function(e){if(e.target===mask){mask.remove();}};
  document.body.appendChild(mask);
  setTimeout(function(){document.getElementById('finNewPwd').focus();},100);
}
function finDoSetPwd(){
  var oldPwd=document.getElementById('finOldPwd')?document.getElementById('finOldPwd').value:'';
  var newPwd=document.getElementById('finNewPwd').value;
  var newPwd2=document.getElementById('finNewPwd2').value;
  if(!newPwd||newPwd.length<4){showToast('⚠️ 密码至少4位');return;}
  if(newPwd!==newPwd2){showToast('⚠️ 两次密码不一致');return;}
  var storedPwd=localStorage.getItem('fin_pwd')||'';
  if(oldPwd&&storedPwd&&oldPwd!==storedPwd){showToast('❌ 旧密码错误');return;}
  localStorage.setItem('fin_pwd',newPwd);
  var mask=document.querySelector('.modal-mask');
  if(mask)mask.remove();
  showToast('✅ 密码设置成功');
}
function finClearPwd(){
  if(!confirm('确定清除密码？清除后财务管家将不再需要验证。'))return;
  localStorage.removeItem('fin_pwd');
  localStorage.removeItem('fin_remember');
  sessionStorage.removeItem('fin_auth');
  showToast('✅ 密码已清除');
  finRender();
}
"""
    # 插入到 </script> 前
    html = html.replace('</script>', new_funcs + '\n  </script>')
    print('[OK] 添加 finShowSetPwdModal/finDoSetPwd/finClearPwd 函数')
else:
    print('[OK] finShowSetPwdModal 已存在')

# 3. 检查 openFinance 逻辑是否正确
if 'function openFinance(' in html:
    # 确保调用 finTryAuth
    if 'finTryAuth' in html:
        print('[OK] finTryAuth 已存在')
    else:
        print('[X] finTryAuth 函数未找到！')

# 写回文件
open('index.html', 'w', encoding='utf-8').write(html)
print('\n完成！文件已更新')

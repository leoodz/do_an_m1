from project import app
from flask import render_template, request, Markup, url_for, redirect , session
from datetime import datetime

from project.xu_ly.xuLy_quan_ly_ban_hang import *

@app.route('/quan-ly-ban-hang/dang-nhap',methods = ['GET','POST'])
def qlbh_dn():
    tendn = ''
    ketqua =''
    if request.method == 'POST':
        result = request.form
        tendn = result.get('TH_tenDN')
        mat_khau = result.get('TH_matkhau')
        nhanvien = Thong_tin_nhan_vien(tendn, mat_khau)
        if nhanvien == None:
            ketqua = "Dang nhap khong thanh cong"
        else:
            session['quan_ly_ban_hang'] = nhanvien
            return redirect('/quan-ly-ban-hang')

    return render_template("quan_ly_ban_hang/dang_nhap.html",tendn = tendn,ketqua = ketqua)

@app.route('/quan-ly-ban-hang',methods = ['GET','POST'])
def qlbh():
    if session.get('quan_ly_ban_hang') == None:
        return redirect('/quan-ly-ban-hang/dang-nhap')
    chuoi_tim =''
    danh_sach_Tivi = Doc_danh_sach_Tivi()
    if request.method == 'POST':
        result = request.form
        chuoi_tim = result.get('TH_gt_tim')
        danh_sach_Tivi = Tra_cuu_Tivi(chuoi_tim,danh_sach_Tivi)

    return render_template("quan_ly_ban_hang/index.html",danh_sach_tivi = danh_sach_Tivi,chuoi_tim = chuoi_tim)


@app.route('/quan-ly-ban-hang/cap-nhat/<string:Ma_so>/',methods = ['GET','POST'])
def qlbh_bh(Ma_so):
    if session.get('quan_ly_ban_hang') == None:
        return redirect('/quan_ly_ban_hang/dang-nhap')
    thong_bao = ''
    sl = 0
    tivi = Thong_tin_tivi(Ma_so)
    phieunhap = ''
    dangxuat = ''
    if request.method == 'GET':
        result = request.form
        capnhat = request.values.get('TH_Cap_Nhat')
        dangxuat = request.values.get('TH_Dang_Xuat')
        if "capnhat" == capnhat:
            return redirect('/quan-ly-ban-hang/thong-ke-phieu-nhap')
        if 'dangxuat' == dangxuat:
            session.pop('quan_ly_ban_hang')
            return redirect('/quan-ly-ban-hang/dang-nhap')
    if tivi == None:
        thong_bao = Ma_so +' khong ton tai'
    elif request.method == 'POST':
        result = request.form
        sl = int(result.get('TH_Don_Gia_Moi'))
        if sl == 0:
            thong_bao ='So luong ko hop le'
        else:
            tivi['Don_gia_Ban'] =  sl
            qlbh = session.get('quan_ly_ban_hang')
            nv ={ "Ho_ten":qlbh['Ho_ten'],"Ma_so":qlbh['Ho_ten']}
            
            Ngay = datetime.now()

            Cap_Nhat = tivi["Don_gia_Ban"] = sl
            tivi["Don_gia_Ban"] = Cap_Nhat
            Ghi_Tivi(tivi)
            thong_bao = 'Đã cập nhật đơn giá'
    return render_template("quan_ly_ban_hang/cap_nhat.html",tivi = tivi,thong_bao = thong_bao,sl = sl,phieunhap=phieunhap, dangxuat=dangxuat)

@app.route('/quan-ly-ban-hang/thong-ke-so-luong-ton',methods = ['GET','POST'])
def qlbh_slt():
    if session.get('quan_ly_ban_hang') == None:
        return redirect('/quan-ly-ban-hang/dang-nhap')
    Nhom = Dem_LT_toan_bo_nhom()
    return render_template("quan_ly_ban_hang/so_luong_ton.html",Nhom = Nhom)


    
    return render_template("quan_ly_ban_hang/danh_sach_ban.html",danh_sach_tivi_nhap=danh_sach_tivi_nhap,tong_tien=tong_tien)

@app.route('/quan-ly-ban-hang/thong-ke-phieu-ban',methods = ['GET','POST'])
def qlbh_dsb():
    if session.get('quan_ly_ban_hang') == None:
        return redirect('/quan-ly-ban-hang/dang-nhap')
    Ngay = datetime.now()
    nvdn = session.get('nhan_vien_ban_hang')
    danh_sach_tivi_nhap , tong_tien = Thong_Ke_Ban_Hang()
    
    return render_template("quan_ly_ban_hang/danh_sach_ban.html",danh_sach_tivi_nhap=danh_sach_tivi_nhap,tong_tien=tong_tien)
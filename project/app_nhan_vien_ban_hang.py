from project import app
from flask import render_template, request, Markup, url_for, redirect , session
from datetime import datetime
from project.xu_ly.xuLy_nhan_vien_ban_hang import *


@app.route('/nhan-vien-ban-hang/dang-nhap',methods = ['GET','POST'])
def nvbh_dn():
    tendn = ''
    ketqua =''
    if request.method == 'POST':
        result = request.form
        tendn = result.get('TH_tenDN')
        mat_khau = result.get('TH_matkhau')
        nhanvien = Thong_tin_nhan_vien(tendn,mat_khau)
        if nhanvien == None:
            ketqua = "Dang nhap khong thanh cong"
        else:
            session['nhan_vien_ban_hang'] = nhanvien
            return redirect('/nhan-vien-ban-hang')

    return render_template("nhan_vien_ban_hang/dang_nhap.html",tendn = tendn,ketqua = ketqua)

@app.route('/nhan-vien-ban-hang',methods = ['GET','POST'])
def nvbh():
    if session.get('nhan_vien_ban_hang') == None:
        return redirect('/nhan-vien-ban-hang/dang-nhap')
    chuoi_tim =''
    danh_sach_Tivi = Doc_danh_sach_Tivi()
    if request.method == 'POST':
        result = request.form
        chuoi_tim = result.get('TH_gt_tim')
        danh_sach_Tivi = Tra_cuu_Tivi(chuoi_tim,danh_sach_Tivi)

    return render_template("nhan_vien_ban_hang/index.html",danh_sach_tivi = danh_sach_Tivi,chuoi_tim = chuoi_tim)



@app.route('/nhan-vien-ban-hang/ban-hang/<string:Ma_so>/',methods = ['GET','POST'])
def nvbh_nh(Ma_so):
    if session.get('nhan_vien_ban_hang') == None:
        return redirect('/nhan-vien-ban-hang/dang-nhap')
    thong_bao = ''
    sl = 0
    tivi = Thong_tin_tivi(Ma_so)
    phieuban = ''
    dangxuat = ''
    if request.method == 'GET':
        result = request.form
        phieuban = request.values.get('TH_Phieu_Ban')
        dangxuat = request.values.get('TH_Dang_Xuat')
        if "phieuban" == phieuban:
            return redirect('/nhan-vien-ban-hang/thong-ke-phieu-ban')
        if 'dangxuat' == dangxuat:
            session.pop('nhan_vien_ban_hang')
            return redirect('/nhan-vien-ban-hang/dang-nhap')
    if tivi == None:
        thong_bao = Ma_so +' khong ton tai'
    elif request.method == 'POST':
        result = request.form
        sl = int(result.get('TH_SoLuong'))
        if sl <= 0:
            thong_bao ='So luong ko hop le'
        else:
            tivi['So_luong_Ton'] =  tivi['So_luong_Ton'] -sl
            nvnp = session.get('nhan_vien_ban_hang')
            nv ={ "Ho_ten":nvnp['Ho_ten'],"Ma_so":nvnp['Ho_ten']}
            
            Ngay = datetime.now()
            
            phieu_ban ={"Ngay": Ngay.strftime('%d-%m-%Y'),"So_luong": sl,"Don_gia": tivi['Don_gia_Nhap'],
            "Tien":tivi['Don_gia_Nhap']*sl,"Nhan_vien":{"Ho_ten": "Nguyễn thị bé Nhỏ","Ma_so": "NV_1"}}

            Danh_sach_Phieu_Ban =tivi['Danh_sach_Phieu_Ban']
            Danh_sach_Phieu_Ban.append(phieu_ban)
            tivi['Danh_sach_Phieu_Ban']= Danh_sach_Phieu_Ban

            Ghi_Tivi(tivi)
            thong_bao = 'Da luu phieu ban'
            return redirect('/nhan-vien-ban-hang/thong-ke-phieu-ban')
    return render_template("nhan_vien_ban_hang/ban_hang.html",tivi = tivi,thong_bao = thong_bao,sl = sl,phieuban=phieuban, dangxuat=dangxuat)

@app.route('/nhan-vien-ban-hang/thong-ke-phieu-ban',methods = ['GET','POST'])
def nvbh_tkpn():
    if session.get('nhan_vien_ban_hang') == None:
        return redirect('/nhan-vien-ban-hang/dang-nhap')
    Ngay = datetime.now()
    nvdn = session.get('nhan_vien_ban_hang')
    danh_sach_tivi_nhap , tong_tien = Thong_Ke_Ban_Hang(Ngay.strftime('%d-%m-%Y'),nvdn['Ma_so'])
    
    return render_template("nhan_vien_ban_hang/phieu_ban.html",danh_sach_tivi_nhap=danh_sach_tivi_nhap,tong_tien=tong_tien)



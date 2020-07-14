from project import app
from flask import render_template, request, Markup, url_for, redirect , session
from datetime import datetime

from project.xu_ly.xuLy_nhan_vien_nhap_hang import *

@app.route('/nhan-vien-nhap-hang/dang-nhap',methods = ['GET','POST'])
def nvnh_dn():
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
            session['nhan_vien_nhap_hang'] = nhanvien
            return redirect('/nhan-vien-nhap-hang')

    return render_template("nhan_vien_nhap_hang/dang_nhap.html",tendn = tendn,ketqua = ketqua)

@app.route('/nhan-vien-nhap-hang',methods = ['GET','POST'])
def nvnh():
    if session.get('nhan_vien_nhap_hang') == None:
        return redirect('/nhan-vien-nhap-hang/dang-nhap')
    chuoi_tim =''
    danh_sach_Tivi = Doc_danh_sach_Tivi()
    if request.method == 'POST':
        result = request.form
        chuoi_tim = result.get('TH_gt_tim')
        danh_sach_Tivi = Tra_cuu_Tivi(chuoi_tim,danh_sach_Tivi)

    return render_template("nhan_vien_nhap_hang/index.html",danh_sach_tivi = danh_sach_Tivi,chuoi_tim = chuoi_tim)


@app.route('/nhan-vien-nhap-hang/nhap-hang/<string:Ma_so>/',methods = ['GET','POST'])
def nvnh_nh(Ma_so):
    if session.get('nhan_vien_nhap_hang') == None:
        return redirect('/nhan-vien-nhap-hang/dang-nhap')
    thong_bao = ''
    sl = 0
    tivi = Thong_tin_tivi(Ma_so)
    phieunhap = ''
    dangxuat = ''
    if request.method == 'GET':
        result = request.form
        phieunhap = request.values.get('TH_Phieu_Nhap')
        dangxuat = request.values.get('TH_Dang_Xuat')
        if "phieunhap" == phieunhap:
            return redirect('/nhan-vien-nhap-hang/thong-ke-phieu-nhap')
        if 'dangxuat' == dangxuat:
            session.pop('nhan_vien_nhap_hang')
            return redirect('/nhan-vien-nhap-hang/dang-nhap')
    if tivi == None:
        thong_bao = Ma_so +' khong ton tai'
    elif request.method == 'POST':
        result = request.form
        sl = int(result.get('TH_SoLuong'))
        if sl == 0:
            thong_bao ='So luong ko hop le'
        else:
            tivi['So_luong_Ton'] =  tivi['So_luong_Ton'] +sl
            nvnp = session.get('nhan_vien_nhap_hang')
            nv ={ "Ho_ten":nvnp['Ho_ten'],"Ma_so":nvnp['Ho_ten']}
            
            Ngay = datetime.now()
            
            phieu_nhap ={"Ngay": Ngay.strftime('%d-%m-%Y'),"So_luong": sl,"Don_gia": tivi['Don_gia_Nhap'],
            "Tien":tivi['Don_gia_Nhap']*sl,"Nhan_vien":{"Ho_ten": "Nguyễn thị bé Nhỏ","Ma_so": "NV_1"}}

            Danh_sach_Phieu_Nhap =tivi['Danh_sach_Phieu_Nhap']
            Danh_sach_Phieu_Nhap.append(phieu_nhap)
            tivi['Danh_sach_Phieu_Nhap']= Danh_sach_Phieu_Nhap

            Ghi_Tivi(tivi)
            thong_bao = 'Da luu phieu nhap'
            return redirect('/nhan-vien-nhap-hang/thong-ke-phieu-nhap')
    return render_template("nhan_vien_nhap_hang/nhap_hang.html",tivi = tivi,thong_bao = thong_bao,sl = sl,phieunhap=phieunhap, dangxuat=dangxuat)

@app.route('/nhan-vien-nhap-hang/thong-ke-phieu-nhap',methods = ['GET','POST'])
def nvnh_tkpn():
    if session.get('nhan_vien_nhap_hang') == None:
        return redirect('/nhan-vien-nhap-hang/dang-nhap')
    Ngay = datetime.now()
    nvdn = session.get('nhan_vien_nhap_hang')
    danh_sach_tivi_nhap , tong_tien =Thong_Ke_Nhap_Hang(Ngay.strftime('%d-%m-%Y'),nvdn['Ma_so'])
    
    return render_template("nhan_vien_nhap_hang/phieu_nhap.html",danh_sach_tivi_nhap=danh_sach_tivi_nhap,tong_tien=tong_tien)



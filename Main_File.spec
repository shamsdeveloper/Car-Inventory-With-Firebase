# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Main_File.py'],
    pathex=[],
    binaries=[],
    datas=[('racing_car.png', '.'), ('serviceAccountKey.json', '.'), ('Images/Frame 422.png', 'Images'), ('Images/my.gif', 'Images'), ('Images/Header.png', 'Images'), ('Images/Blur_image.png', 'Images'), ('Images/Admin_image.png', 'Images'), ('Images/car_window_icon.png', 'Images'), ('dashboard_images/car_inventory.png', 'dashboard_images'), ('dashboard_images/admin_user.png', 'dashboard_images'), ('dashboard_images/search.png', 'dashboard_images'), ('dashboard_images/teamwork.png', 'dashboard_images'), ('dashboard_images/report_header.jpg', 'dashboard_images'), ('Side_bar_icon/home.png', 'Side_bar_icon'), ('Side_bar_icon/sale.png', 'Side_bar_icon'), ('Side_bar_icon/purchase.png', 'Side_bar_icon'), ('Side_bar_icon/employee.png', 'Side_bar_icon'), ('Side_bar_icon/inventory.png', 'Side_bar_icon'), ('Side_bar_icon/financial.png', 'Side_bar_icon'), ('Side_bar_icon/report.png', 'Side_bar_icon'), ('Side_bar_icon/admin.png', 'Side_bar_icon'), ('Side_bar_icon/logut.png', 'Side_bar_icon'), ('card_images/sold_2156144.png', 'card_images'), ('card_images/car_554392.png', 'card_images'), ('card_images/borrow_3707947.png', 'card_images'), ('card_images/car_shop.png', 'card_images'), ('card_images/my_bottom.PNG', 'card_images'), ('card_images/my_bottom1.PNG', 'card_images'), ('card_images/desc.PNG', 'card_images'), ('car_loading.gif', '.'), ('welcome_screen.py', '.'), ('material.xml', '.'), ('material.qss', '.'), ('Dashboard.py', '.'), ('Login_Registration_Form.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt6', 'PySide6'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Main_File',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['Car_Inventory.ico'],
)

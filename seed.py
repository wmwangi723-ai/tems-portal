from app import create_app, db
from app.models import User, Level, Module, Unit

UNITS_DATA = {
    1: ["INSTALL CONDUIT SYSTEM", "INSTALL PVC SHEATHED CABLE SYSTEM", "INSTALL TRUNKING SYSTEM"],
    2: ["INSTALL STAND-ALONE SOLAR PV SYSTEMS", "PERFORM BELL AND ALARM INSTALLATION", "WIND ELECTRICAL MACHINE"],
    3: ["APPLY BASIC ELECTRICAL PRINCIPLES", "APPLY COMMUNICATION SKILLS", "APPLY DIGITAL LITERACY", "PERFORM ELECTRICAL INSTALLATION", "PREPARE TECHNICAL DRAWINGS"],
    4: ["APPLY ANALOGUE ELECTRONICS I", "APPLY DIGITAL ELECTRONICS I", "APPLY ENGINEERING TECHNICIAN MATHEMATICS I", "APPLY WORK ETHICS AND PRACTICES", "PERFORM SECURITY SYSTEM INSTALLATION"],
    5: ["APPLY ANALOGUE ELECTRONICS II", "APPLY DIGITAL ELECTRONICS II", "APPLY ENGINEERING TECHNICIAN MATHEMATICS II", "APPLY ENTREPRENEURIAL SKILLS", "INSTALL SOLAR PV SYSTEMS", "PERFORM ELECTRICAL MACHINE INSTALLATION"],
    6: ["APPLY ELECTRICAL PRINCIPLES I", "APPLY ENGINEERING TECHNICIAN MATHEMATICS III", "APPLY MICRO CONTROL SYSTEMS", "INSTALL ELECTRICAL POWER LINES"],
    7: ["APPLY CONTROL SYSTEMS", "APPLY ELECTRICAL PRINCIPLES II", "APPLY ENGINEERING TECHNICIAN MATHEMATICS IV", "AUTOMATE ELECTRICAL SYSTEMS"],
    8: ["APPLY RESEARCH METHODS", "FABRICATE POWER ELECTRONICS CIRCUITS", "PERFORM ELECTRICAL MEASUREMENT AND FAULT DIAGNOSIS", "SUPERVISE ELECTRICAL PROJECT"]
}

LEVEL_ACCESS = {
    3: [1],
    4: [1, 2],
    5: [1, 2, 3, 4, 5],
    6: [1, 2, 3, 4, 5, 6, 7, 8]
}

def run_seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database tables recreated.")

        admin = User(username="admin", is_admin=True)
        admin.set_password("securepassword123")
        db.session.add(admin)

        modules_dict = {}
        for mod_num in range(1, 9):
            mod = Module(module_number=mod_num)
            db.session.add(mod)
            modules_dict[mod_num] = mod
        
        db.session.commit()

        for lvl_num, accessible_mods in LEVEL_ACCESS.items():
            lvl = Level(level_number=lvl_num)
            for mod_num in accessible_mods:
                lvl.modules.append(modules_dict[mod_num])
            db.session.add(lvl)

        for mod_num, units in UNITS_DATA.items():
            current_mod = modules_dict[mod_num]
            for unit_title in units:
                new_unit = Unit(title=unit_title, module=current_mod)
                db.session.add(new_unit)

        db.session.commit()
        print("TEMS Database successfully seeded with CDACC EE Curriculum!")

if __name__ == '__main__':
    run_seed()
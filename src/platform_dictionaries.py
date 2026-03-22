def get_platform_full_name(platform_code):
    """
    Returns the platform's full name
    """
    platform_dict = {
        # 8th Generation
        'PS4': 'PlayStation 4', 'XOne': 'Xbox One', 'WiiU': 'Nintendo Wii U',
        '3DS': 'Nintendo 3DS', 'PSV': 'PlayStation Vita', 'PC': 'Personal Computer',

        # 7th Generation  
        'X360': 'Xbox 360', 'PS3': 'PlayStation 3', 'Wii': 'Nintendo Wii',
        'DS': 'Nintendo DS', 'PSP': 'PlayStation Portable',
        
        # 6th Generation
        'PS2': 'PlayStation 2', 'XB': 'Xbox', 'GC': 'Nintendo GameCube',
        'GBA': 'Game Boy Advance',
        
        # 5th Generation
        'PS': 'PlayStation', 'N64': 'Nintendo 64', 'SAT': 'Sega Saturn',
        'SCD': 'Sega CD/Mega CD',
        
        # 4th Generation
        'SNES': 'Super Nintendo Entertainment System', 'GEN': 'Sega Genesis/Mega Drive',
        'TG16': 'TurboGrafx-16/PC Engine', 'GB': 'Game Boy', 'GG': 'Game Gear',
        
        # 3rd Generation
        'NES': 'Nintendo Entertainment System',
        
        # 2nd Generation
        '2600': 'Atari 2600',
        
        # Otras
        'DC': 'Sega Dreamcast', 'NG': 'Neo Geo', '3DO': '3DO Interactive Multiplayer',
        'PCFX': 'PC-FX', 'WS': 'WonderSwan'
    }
    
    return platform_dict.get(platform_code, 'Unknown')


def get_platform_generation(platform_code):
    """
    Returns the platform's generation
    """
    generation_dict = {
        # 8th Generation (2012-Presente)
        'PS4': '8th Gen', 'XOne': '8th Gen', 'WiiU': '8th Gen', 
        '3DS': '8th Gen', 'PSV': '8th Gen',
        
        # 7th Generation (2005-2012)
        'X360': '7th Gen', 'PS3': '7th Gen', 'Wii': '7th Gen',
        'DS': '7th Gen', 'PSP': '7th Gen',
        
        # 6th Generation (1998-2005)
        'PS2': '6th Gen', 'XB': '6th Gen', 'GC': '6th Gen', 'GBA': '6th Gen',
        
        # 5th Generation (1993-1999)
        'PS': '5th Gen', 'N64': '5th Gen', 'SAT': '5th Gen', 'SCD': '5th Gen',
        
        # 4th Generation (1987-1994)
        'SNES': '4th Gen', 'GEN': '4th Gen', 'TG16': '4th Gen', 
        'GB': '4th Gen', 'GG': '4th Gen',
        
        # 3rd Generation (1983-1989)
        'NES': '3rd Gen',
        
        # 2nd Generation (1976-1984)
        '2600': '2nd Gen',
        
        # Special
        'DC': '6th Gen', 'NG': '4th Gen', '3DO': '5th Gen',
        'PCFX': '5th Gen', 'WS': '5th Gen', 'PC': 'PC'
    }
    
    return generation_dict.get(platform_code, 'Unknown')


def get_platform_type(platform_code):
    """
    Classifies the platforms by: PC, Console or Portable
    """
    platform_type_dict = {
        # === PC ===
        'PC': 'PC',
        
        # === CONSOLAS DOMÉSTICAS PRINCIPALES ===
        # Sony
        'PS': 'Console', 'PS2': 'Console', 'PS3': 'Console', 'PS4': 'Console',
        # Microsoft
        'XB': 'Console', 'X360': 'Console', 'XOne': 'Console',
        # Nintendo
        'NES': 'Console', 'SNES': 'Console', 'N64': 'Console', 'GC': 'Console', 
        'Wii': 'Console', 'WiiU': 'Console',
        # Sega
        'GEN': 'Console', 'SAT': 'Console', 'DC': 'Console',
        # Atari
        '2600': 'Console',
        
        # === CONSOLAS PORTÁTILES ===
        # Nintendo Portable
        'GB': 'Portable', 'GBA': 'Portable', 'DS': 'Portable', '3DS': 'Portable',
        # Sony Portable
        'PSP': 'Portable', 'PSV': 'Portable',
        # Sega Portable
        'GG': 'Portable',
        # Bandai
        'WS': 'Portable',
        
        # === CONSOLAS ESPECIALIZADAS/NICHO ===
        'NG': 'Console',      # Neo Geo - Arcade/Home
        'TG16': 'Console',    # TurboGrafx-16 - Nicho
        '3DO': 'Console',     # 3DO - Multimedia
        'PCFX': 'Console',    # PC-FX - Japón exclusivo
        'SCD': 'Console'      # Sega CD - Add-on/Periférico
    }
    
    return platform_type_dict.get(platform_code, 'Unknown')


def get_platform_company(platform_code):
    """
    Classifies platforms by their company
    """
    company_dict = {
        # === NINTENDO ===
        'NES': 'Nintendo', 'SNES': 'Nintendo', 'N64': 'Nintendo', 'GC': 'Nintendo',
        'Wii': 'Nintendo', 'WiiU': 'Nintendo', 'GB': 'Nintendo', 'GBA': 'Nintendo',
        'DS': 'Nintendo', '3DS': 'Nintendo',
        
        # === SONY ===
        'PS': 'Sony', 'PS2': 'Sony', 'PS3': 'Sony', 'PS4': 'Sony',
        'PSP': 'Sony', 'PSV': 'Sony',
        
        # === MICROSOFT ===
        'XB': 'Microsoft', 'X360': 'Microsoft', 'XOne': 'Microsoft',
        
        # === SEGA ===
        'GEN': 'Sega', 'SAT': 'Sega', 'DC': 'Sega', 'GG': 'Sega', 'SCD': 'Sega',
        
        # === ATARI ===
        '2600': 'Atari',
        
        # === NEO GEO (SNK) ===
        'NG': 'SNK',
        
        # === NEC (Turbografx) ===
        'TG16': 'NEC', 'PCFX': 'NEC',
        
        # === 3DO COMPANY ===
        '3DO': '3DO Company',
        
        # === BANDAI ===
        'WS': 'Bandai',
        
        # === PC (VARIOS FABRICANTES) ===
        'PC': 'Other'
    }
    
    return company_dict.get(platform_code, 'Unknown')

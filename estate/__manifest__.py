{
    'name': "Real Estate",
    
    'depends': ['base'],
    'category': 'Real Estate/Brokerage',
   
    
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',     
        'views/estate_property_menu.xml',
        
        
     
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        
    ],
    'application': True,
    'license': 'LGPL-3'
}


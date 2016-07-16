from sklearn import cross_validation, grid_search, neighbors

def zip_parser(x):
  z = x.split()[-1][:5]
  try:
    zint = int(z)
    if len(z) == 5:
      return z
    else:
      return u''
  except:
    return u''
  
if False:
  df = pd.read_hdf('./data/df_cleaned_res_only.hd5','df')
  df['zipcode'] = df.CITYSTZIP.map(lambda r: zip_parser(r))

  #print df.zipcode.unique()

  # extract zips from CITYSTZIP column
  df['zipcode'] = df.CITYSTZIP.map(lambda r: zip_parser(r))
  

  # Use nearest neighbors to fill in missing
  param_grid = {"n_neighbors": range(4,10)}
  zip_model = grid_search.GridSearchCV( neighbors.KNeighborsClassifier(),
                  param_grid=param_grid,
                  cv=cross_validation.ShuffleSplit(len(df.index), n_iter=20, 
                      test_size=0.2,random_state=42) )

  zip_model.fit(df[['latitude','longitude']],df['zipcode'])
  for key in param_grid.keys():
    grid_score_plotter(zip_model,key)

  badzip = df.zipcode==''
  df.loc[badzip,'zipcode'] = zip_model.predict(df.loc[badzip,('latitude','longitude')])
  
  df.to_hdf('./data/df_cleaned_zipcodes.hd5','df')

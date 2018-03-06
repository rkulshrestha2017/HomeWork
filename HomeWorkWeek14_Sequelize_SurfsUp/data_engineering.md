
## Data Engineering


```python
import pandas as pd
import numpy as np
```


```python
measurements_df = pd.read_csv("Resources/hawaii_measurements.csv")
stations_df = pd.read_csv("Resources/hawaii_stations.csv")
```


```python
measurements_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>station</th>
      <th>date</th>
      <th>prcp</th>
      <th>tobs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USC00519397</td>
      <td>2010-01-01</td>
      <td>0.08</td>
      <td>65</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USC00519397</td>
      <td>2010-01-02</td>
      <td>0.00</td>
      <td>63</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USC00519397</td>
      <td>2010-01-03</td>
      <td>0.00</td>
      <td>74</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USC00519397</td>
      <td>2010-01-04</td>
      <td>0.00</td>
      <td>76</td>
    </tr>
    <tr>
      <th>4</th>
      <td>USC00519397</td>
      <td>2010-01-06</td>
      <td>NaN</td>
      <td>73</td>
    </tr>
  </tbody>
</table>
</div>




```python
stations_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>station</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>elevation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USC00519397</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.2716</td>
      <td>-157.8168</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USC00513117</td>
      <td>KANEOHE 838.1, HI US</td>
      <td>21.4234</td>
      <td>-157.8015</td>
      <td>14.6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USC00514830</td>
      <td>KUALOA RANCH HEADQUARTERS 886.9, HI US</td>
      <td>21.5213</td>
      <td>-157.8374</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USC00517948</td>
      <td>PEARL CITY, HI US</td>
      <td>21.3934</td>
      <td>-157.9751</td>
      <td>11.9</td>
    </tr>
    <tr>
      <th>4</th>
      <td>USC00518838</td>
      <td>UPPER WAHIAWA 874.3, HI US</td>
      <td>21.4992</td>
      <td>-158.0111</td>
      <td>306.6</td>
    </tr>
  </tbody>
</table>
</div>




```python
measurements_df[pd.isnull(measurements_df).any(axis=1)]
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>station</th>
      <th>date</th>
      <th>prcp</th>
      <th>tobs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4</th>
      <td>USC00519397</td>
      <td>2010-01-06</td>
      <td>NaN</td>
      <td>73</td>
    </tr>
    <tr>
      <th>26</th>
      <td>USC00519397</td>
      <td>2010-01-30</td>
      <td>NaN</td>
      <td>70</td>
    </tr>
    <tr>
      <th>29</th>
      <td>USC00519397</td>
      <td>2010-02-03</td>
      <td>NaN</td>
      <td>67</td>
    </tr>
    <tr>
      <th>43</th>
      <td>USC00519397</td>
      <td>2010-02-19</td>
      <td>NaN</td>
      <td>63</td>
    </tr>
    <tr>
      <th>61</th>
      <td>USC00519397</td>
      <td>2010-03-11</td>
      <td>NaN</td>
      <td>73</td>
    </tr>
    <tr>
      <th>72</th>
      <td>USC00519397</td>
      <td>2010-03-26</td>
      <td>NaN</td>
      <td>72</td>
    </tr>
    <tr>
      <th>122</th>
      <td>USC00519397</td>
      <td>2010-05-21</td>
      <td>NaN</td>
      <td>77</td>
    </tr>
    <tr>
      <th>176</th>
      <td>USC00519397</td>
      <td>2010-07-16</td>
      <td>NaN</td>
      <td>78</td>
    </tr>
    <tr>
      <th>282</th>
      <td>USC00519397</td>
      <td>2010-11-04</td>
      <td>NaN</td>
      <td>73</td>
    </tr>
    <tr>
      <th>294</th>
      <td>USC00519397</td>
      <td>2010-11-19</td>
      <td>NaN</td>
      <td>72</td>
    </tr>
    <tr>
      <th>324</th>
      <td>USC00519397</td>
      <td>2010-12-26</td>
      <td>NaN</td>
      <td>74</td>
    </tr>
    <tr>
      <th>341</th>
      <td>USC00519397</td>
      <td>2011-01-13</td>
      <td>NaN</td>
      <td>68</td>
    </tr>
    <tr>
      <th>369</th>
      <td>USC00519397</td>
      <td>2011-02-12</td>
      <td>NaN</td>
      <td>68</td>
    </tr>
    <tr>
      <th>390</th>
      <td>USC00519397</td>
      <td>2011-03-08</td>
      <td>NaN</td>
      <td>72</td>
    </tr>
    <tr>
      <th>490</th>
      <td>USC00519397</td>
      <td>2011-06-24</td>
      <td>NaN</td>
      <td>77</td>
    </tr>
    <tr>
      <th>586</th>
      <td>USC00519397</td>
      <td>2011-10-05</td>
      <td>NaN</td>
      <td>79</td>
    </tr>
    <tr>
      <th>830</th>
      <td>USC00519397</td>
      <td>2012-06-08</td>
      <td>NaN</td>
      <td>77</td>
    </tr>
    <tr>
      <th>831</th>
      <td>USC00519397</td>
      <td>2012-06-09</td>
      <td>NaN</td>
      <td>76</td>
    </tr>
    <tr>
      <th>861</th>
      <td>USC00519397</td>
      <td>2012-07-09</td>
      <td>NaN</td>
      <td>77</td>
    </tr>
    <tr>
      <th>901</th>
      <td>USC00519397</td>
      <td>2012-08-18</td>
      <td>NaN</td>
      <td>77</td>
    </tr>
    <tr>
      <th>902</th>
      <td>USC00519397</td>
      <td>2012-08-19</td>
      <td>NaN</td>
      <td>76</td>
    </tr>
    <tr>
      <th>1011</th>
      <td>USC00519397</td>
      <td>2012-12-06</td>
      <td>NaN</td>
      <td>69</td>
    </tr>
    <tr>
      <th>1012</th>
      <td>USC00519397</td>
      <td>2012-12-07</td>
      <td>NaN</td>
      <td>69</td>
    </tr>
    <tr>
      <th>1045</th>
      <td>USC00519397</td>
      <td>2013-01-10</td>
      <td>NaN</td>
      <td>72</td>
    </tr>
    <tr>
      <th>1046</th>
      <td>USC00519397</td>
      <td>2013-01-11</td>
      <td>NaN</td>
      <td>72</td>
    </tr>
    <tr>
      <th>1240</th>
      <td>USC00519397</td>
      <td>2013-07-24</td>
      <td>NaN</td>
      <td>79</td>
    </tr>
    <tr>
      <th>1410</th>
      <td>USC00519397</td>
      <td>2014-01-10</td>
      <td>NaN</td>
      <td>72</td>
    </tr>
    <tr>
      <th>1411</th>
      <td>USC00519397</td>
      <td>2014-01-11</td>
      <td>NaN</td>
      <td>70</td>
    </tr>
    <tr>
      <th>1528</th>
      <td>USC00519397</td>
      <td>2014-05-08</td>
      <td>NaN</td>
      <td>73</td>
    </tr>
    <tr>
      <th>1529</th>
      <td>USC00519397</td>
      <td>2014-05-09</td>
      <td>NaN</td>
      <td>77</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>19128</th>
      <td>USC00516128</td>
      <td>2016-06-05</td>
      <td>NaN</td>
      <td>73</td>
    </tr>
    <tr>
      <th>19147</th>
      <td>USC00516128</td>
      <td>2016-06-25</td>
      <td>NaN</td>
      <td>73</td>
    </tr>
    <tr>
      <th>19152</th>
      <td>USC00516128</td>
      <td>2016-07-01</td>
      <td>NaN</td>
      <td>74</td>
    </tr>
    <tr>
      <th>19153</th>
      <td>USC00516128</td>
      <td>2016-07-04</td>
      <td>NaN</td>
      <td>74</td>
    </tr>
    <tr>
      <th>19170</th>
      <td>USC00516128</td>
      <td>2016-07-23</td>
      <td>NaN</td>
      <td>74</td>
    </tr>
    <tr>
      <th>19181</th>
      <td>USC00516128</td>
      <td>2016-08-03</td>
      <td>NaN</td>
      <td>74</td>
    </tr>
    <tr>
      <th>19182</th>
      <td>USC00516128</td>
      <td>2016-08-04</td>
      <td>NaN</td>
      <td>74</td>
    </tr>
    <tr>
      <th>19183</th>
      <td>USC00516128</td>
      <td>2016-08-05</td>
      <td>NaN</td>
      <td>75</td>
    </tr>
    <tr>
      <th>19184</th>
      <td>USC00516128</td>
      <td>2016-08-06</td>
      <td>NaN</td>
      <td>77</td>
    </tr>
    <tr>
      <th>19204</th>
      <td>USC00516128</td>
      <td>2016-08-27</td>
      <td>NaN</td>
      <td>74</td>
    </tr>
    <tr>
      <th>19287</th>
      <td>USC00516128</td>
      <td>2016-11-20</td>
      <td>NaN</td>
      <td>74</td>
    </tr>
    <tr>
      <th>19314</th>
      <td>USC00516128</td>
      <td>2016-12-18</td>
      <td>NaN</td>
      <td>67</td>
    </tr>
    <tr>
      <th>19361</th>
      <td>USC00516128</td>
      <td>2017-02-04</td>
      <td>NaN</td>
      <td>66</td>
    </tr>
    <tr>
      <th>19374</th>
      <td>USC00516128</td>
      <td>2017-02-18</td>
      <td>NaN</td>
      <td>72</td>
    </tr>
    <tr>
      <th>19396</th>
      <td>USC00516128</td>
      <td>2017-03-13</td>
      <td>NaN</td>
      <td>69</td>
    </tr>
    <tr>
      <th>19400</th>
      <td>USC00516128</td>
      <td>2017-03-18</td>
      <td>NaN</td>
      <td>70</td>
    </tr>
    <tr>
      <th>19412</th>
      <td>USC00516128</td>
      <td>2017-03-31</td>
      <td>NaN</td>
      <td>76</td>
    </tr>
    <tr>
      <th>19419</th>
      <td>USC00516128</td>
      <td>2017-04-08</td>
      <td>NaN</td>
      <td>76</td>
    </tr>
    <tr>
      <th>19444</th>
      <td>USC00516128</td>
      <td>2017-05-04</td>
      <td>NaN</td>
      <td>74</td>
    </tr>
    <tr>
      <th>19459</th>
      <td>USC00516128</td>
      <td>2017-05-20</td>
      <td>NaN</td>
      <td>70</td>
    </tr>
    <tr>
      <th>19468</th>
      <td>USC00516128</td>
      <td>2017-05-30</td>
      <td>NaN</td>
      <td>72</td>
    </tr>
    <tr>
      <th>19470</th>
      <td>USC00516128</td>
      <td>2017-06-03</td>
      <td>NaN</td>
      <td>74</td>
    </tr>
    <tr>
      <th>19476</th>
      <td>USC00516128</td>
      <td>2017-06-10</td>
      <td>NaN</td>
      <td>72</td>
    </tr>
    <tr>
      <th>19528</th>
      <td>USC00516128</td>
      <td>2017-08-01</td>
      <td>NaN</td>
      <td>72</td>
    </tr>
    <tr>
      <th>19531</th>
      <td>USC00516128</td>
      <td>2017-08-05</td>
      <td>NaN</td>
      <td>77</td>
    </tr>
    <tr>
      <th>19532</th>
      <td>USC00516128</td>
      <td>2017-08-06</td>
      <td>NaN</td>
      <td>79</td>
    </tr>
    <tr>
      <th>19537</th>
      <td>USC00516128</td>
      <td>2017-08-11</td>
      <td>NaN</td>
      <td>72</td>
    </tr>
    <tr>
      <th>19539</th>
      <td>USC00516128</td>
      <td>2017-08-13</td>
      <td>NaN</td>
      <td>80</td>
    </tr>
    <tr>
      <th>19544</th>
      <td>USC00516128</td>
      <td>2017-08-18</td>
      <td>NaN</td>
      <td>76</td>
    </tr>
    <tr>
      <th>19546</th>
      <td>USC00516128</td>
      <td>2017-08-20</td>
      <td>NaN</td>
      <td>78</td>
    </tr>
  </tbody>
</table>
<p>1447 rows × 4 columns</p>
</div>




```python
len(measurements_df)
```




    19550



About 7.5% of the precipition data is NaN, dates are missing, no temp data missing


```python
stations_df[pd.isnull(stations_df).any(axis=1)]
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>station</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>elevation</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>



No data missing in station file


```python
measurements_df.to_csv("clean_measurements.csv", index = False)
```


```python
stations_df.to_csv("clean_stations.csv", index = False)
```
